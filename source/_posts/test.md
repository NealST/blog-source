---
title: 用多集群事件导出器打通企业自动化的最后一公里
date: 2026-04-01 18:00:00
tags:
  - AI-engineering
  - cloudflare
categories: tools
---

> 原文：[Implement a multicluster event exporter for enterprise automation](https://developers.redhat.com/articles/2026/04/01/implement-multicluster-event-exporter-enterprise-automation)，作者 Meng Yan

---

管理一两个 Kubernetes 集群，靠 kubectl 就够了。但当你手里有几百个集群、分布在十几个 hub 上时，「靠人盯」这件事就彻底不现实了。

这篇文章想聊的，是 Red Hat Advanced Cluster Management 里一个相对低调的组件——多集群全局 hub agent——以及它最近被拓展出来的一个新能力：作为事件导出器，把集群生命周期事件推送给企业里的任何自动化系统。

## 问题出在哪里

在大规模多集群环境里，事件数据是运维和自动化的基础原料。但现状很割裂。

每个 RHACM hub 的事件只存在本地，运维团队要看就得逐个登录。十几个 hub、每个 hub 管着几百个集群，手动巡检根本跟不上节奏。

Kubernetes 原生事件的格式也不统一。`ManagedCluster` 事件是一套结构，`ClusterDeployment` 又是另一套，`Policy` 再换一套。下游系统消费这些事件，就得为每种格式单独写解析逻辑，维护起来很头疼。

Ansible Automation Platform、Splunk 这类企业自动化工具根本无法直接抓取 Kubernetes 集群事件，没有标准化的事件流，工作流就只能靠轮询 API 或者手搓集成来凑合，既慢又脆。

还有一个更具体的痛点：用 Hive 创建集群，整个过程可能要 40 分钟以上，但期间几乎没有任何事件覆盖。操作员只能干等，完全不知道进度到哪里、哪个环节出了问题。

## Agent 的两个身份

多集群全局 hub agent 部署在每个被管 hub 上，原本的职责是作为分布式控制平面：接收全局 hub manager 的配置下发，把集群状态和策略合规数据同步回去，供 Grafana 做跨 hub 的可视化。

现在它多了第二个身份：独立的事件导出器。两个角色是解耦的，不用全局 hub 的控制平面能力，也可以单独启用事件导出。

## 事件是怎么流动的

agent 做的事拆开来看分三步。

先是收集。它监听 hub 上各类资源的状态变化，不只是 Kubernetes Events 资源，`ManagedCluster` 的状态转换、策略合规更新、`ClusterGroupUpgrade` 的进度，都在范围内。

然后是转换。原始 Kubernetes 事件里有大量底层细节，agent 过滤出有业务意义的信息（集群名、事件原因、合规状态、创建进度），封装成 [CloudEvents](https://cloudevents.io/) 格式。CloudEvents 是 CNCF 的标准规范，解决的就是跨系统事件互通的问题。

最后发布到 Kafka。全局 hub manager 从这里消费事件存入数据库，但任何外部系统都可以同时订阅同一个 topic。

设计上有一个关键点：agent 只管收集和标准化，不关心谁在消费。消费方订阅 Kafka 就行，不需要懂 RHACM 或 Hive 的内部结构。

## 事件都有哪些

### 集群生命周期事件

集群从创建到销毁，每个关键节点都有对应事件：

- `ProvisionStarted`：Hive 开始创建集群
- `ProvisionCompleted`：集群创建完成
- `ProvisionFailed`：创建失败
- `Imported`：集群成功导入 hub
- `Detaching`：集群开始从 hub 解绑

每个事件都是 CloudEvents 格式，包含三层信息：事件元数据（类型、来源 hub、发生时间）、Kafka 传输元数据（topic、partition、offset），以及业务数据（集群名、集群 ID、所属 hub、事件原因和可读描述）。

一个典型的 `Detaching` 事件长这样：

```
Context Attributes,
  type: io.open-cluster-management.operator.multiclusterglobalhubs.event.managedcluster
  source: hub1
  id: 49aa624c-c3d9-4016-9c7d-23c5825a4fef
  time: 2025-10-23T02:34:36.943743765Z

Data,
  {
    "clusterName": "cluster1",
    "leafHubName": "hub1",
    "message": "The cluster1 is currently becoming detached",
    "reason": "Detaching",
    "reportingController": "managedcluster-import-controller"
  }
```

### 策略状态事件

策略事件记录集群合规状态的变化：`Compliant`（通过检查）、`NonCompliant`（违反策略）、`PolicyStatusSync`（同步进行中）。事件里带有策略 ID、集群 ID 和具体违规原因，消费方可以精确定位到哪条策略在哪个集群上出了什么问题。

## 能用来做什么

舰队级的集群状态追踪是最直接的用例——实时看哪些集群还在创建中，创建时间超过阈值就告警，这类事情以前要专门写采集脚本，现在订阅 Kafka topic 就能搞定。

Day 2 运维也可以完全自动化。集群 `Imported` 之后，下游按顺序自动跑：配存储类、起监控和日志 agent、推安全策略、更新 CMDB。之前这些步骤要靠人盯着新集群上线通知，现在事件来了自动触发。

`ProvisionFailed` 的处理是类似思路：自动收集诊断信息，清理孤儿云资源，开故障工单，条件合适就重试。Ansible EDA 在这里很顺手，Rulebook 里匹配 `event.body.reason == "Imported"` 就行，不需要额外的适配层。

## 小结

问题的核心是集群事件被困在每个 hub 里出不来，导致企业的自动化系统无从接入。CloudEvents + Kafka 这个组合，让集群事件变成了整个基础设施层可以共享的数据流，任何 Kafka 消费者都可以接入。官方说这套机制已经在 3500+ 集群规模下跑通了。

代码仓库在 [multicluster global hub repo](https://github.com/stolostron/multicluster-global-hub)，还有一篇用 TALM 事件配合 Event Driven Ansible 的实战文章可以参考：[Leveraging TALM Events for Automated Workflows with Event Driven Ansible in OpenShift](https://access.redhat.com/articles/7120537)。

