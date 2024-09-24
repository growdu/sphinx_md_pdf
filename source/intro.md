---
sidebar_position: 1
---

# KingbaseES介绍

欢迎使用金仓数据库管理系统KingbaseES V8产品文档。

金仓数据库管理系统，简称KingbaseES，是北京人大金仓信息技术股份有限公司[简称人大金仓]的核心产品，具有大型通用、"三高"（高可靠、高性能、高安全）、"三易"（易管理、易使用、易扩展）、运行稳定等特点，是唯一入选国家自主创新产品目录的数据库产品，也是国家级、省部级实际项目中应用最广泛的国产数据库产品。

# 特殊格式效果展示

## 告警提示

告警提示使用3个连续的冒号包裹文本来实现。

:::note
这是一个主意事项
:::

:::tip
这是一个使用技巧
:::

:::info
这是一个提示
:::

:::warning
这是一个告警
:::

:::danger
这是一个危险操作
:::


## 选项卡


```mdx-code-block
import Tabs from "@theme/Tabs";
import TabItem from "@theme/TabItem";

<Tabs>
    <TabItem value="rwc" label="读写分离集群" default>       
        - 金仓[读写分离集群](/docs/rwc)是基于硬件、软件系统不可靠，一定会有故障的假设设计的，是基于单台计算机无足够能力处理大量数据设计的。
        
        - 只要数据副本数量大于一，无论是硬件的升级、还是软件的迁移、单机的宕机或软件错误都无需停止对外服务，极大的保证系统的正常运行，并且降低了系统管理员和运维人员的工作量。
    </TabItem>
    <TabItem value="tptc" label="两地三中心集群" default>
        - 两地三中心集群是金仓基于读写分离集群扩展出来的满足金融场景的高可用集群解决方案。

        - 两地三中心集群提供了极致的RTO和RPO能力，系统可用性可以达到99.9999%
    </TabItem>
    <TabItem value="rac" label="RAC共享存储集群" default>
        [KingbaseES RAC](/docs/rac)是人大金仓推出的、完全自主研发的国产共享存储数据库集群，具备稳定、高可用、高性能、高扩展特性。KingbaseES RAC共享存储集群方案可以提供性能扩展和可用性，同时保持低存储成本和中等维护成本，适用于大部分业务的需求。
    </TabItem>
</Tabs>
```
## 行内代码


这是一个行内代码，使用`select * from test` 为例。

## 代码块

代码块上可以添加标题，用三个反引号包裹，在反引号后面加语言和标题。


```jsx title="/src/commponents/hello.js"
function test(props) {
    return <h1>hello</>
}
```

```c title="hello.c"
#include <stdio.h>
int main(void)
{
    printf("hello world\n");
    return 0;
}
```

```java title="hello.java"
class test
{
    public static void main(String []args)
    {
        System.out.println("Hello world");
    }
}
```

```sql title="hello.sql"
select * from test;
select * from pg_stat_replication;
```

## 表格

|特性|特性说明|
|:-------:|:-------:|
| 可靠性 | 高可用解决方案应该包括可靠的硬件，以及可靠的软件（包括数据库，应用服务器，和客户端等）。与可靠性相关的就是可扩展性，比如，通常集群就是由多个普通的硬件在集群软件的控制下协同工作，它的整体性能并不低于价格高昂的大型服务器。另外集群的优势还体现在即使单个节点可能故障的情况下仍能持续的对外提供服务。|
|可恢复性|确定在系统中可能发生什么种类的故障，以及如何尽快从这些故障中恢复对于满足业务对于可用性的需求非常重要。例如当某个数据库的数据所在存储不可用时，应该采取何种措施处理，系统的高可用架构是否支持在SLA约定的时间内从这种故障中恢复。|
|自动故障检测|如果系统中有某个关键组件无法正常工作，系统应能够及时发现并采取相应的补救措施。比如，某个节点的对外网络失效，高可用故障检测软件需要在特定时间内检测到问题，并采取切换服务到另外节点，如果问题在发生数小时后才被发现和处理，可用性将很难保障。|
|连续服务|当进行系统维护且不允许暂停应用时，系统应能够提供持续的服务能力。例如移动数据库的存储位置或者增加硬件，在高可用系统中这些操作都应该是对用户透明的。|

## 链接

- [高可用概述](/docs/ha)
- [基于linux系统的数据库软件安装指南](/docs/linux_install)

## 图片

```mdx-code-block
<Tabs>
    <TabItem value="3az" label="两地三中心方案(同城2AZ+异地1AZ)" default> 
        部署架构：（最少节点2+1+2+1+1，+1仲裁）
        - 生产中心：可用区AZ1，至少3节点，2个数据库节点，1个仲裁节点

        - 同城中心：可用区AZ2，至少3节点，2个数据库节点，1个仲裁节点

        - 异地中心+仲裁中心：可用区AZ3，至少1节点，额外有1个无数据库的仲裁节点  

        其架构图如下：    

        ![3az](../static/img/tptc3az-12211.png)
    </TabItem>
    <TabItem value="2az" label="同城双中心方案(同城2AZ)" default>
        部署架构：（最少节点2+1+2+1）
        - 生产中心：可用区AZ1，至少3节点，2个数据库节点，1个仲裁节点

        - 同城中心：可用区AZ2，至少3节点，2个数据库节点，1个仲裁节点

        其架构图如下：    
        
        ![3az](../static/img/tptc2az-122.png)
    </TabItem>
    <TabItem value="1az" label="同城双中心方案(同城3AZ)" default>
        部署架构：（最少节点2+1+2+1,+1仲裁）
        - 生产中心：可用区AZ1，至少3节点，2个数据库节点，1个仲裁节点

        - 同城中心：可用区AZ2，至少3节点，2个数据库节点，1个仲裁节点

        其架构图如下：        
        
        ![3az](../static/img/tptc3az-1221.png)
    </TabItem>
</Tabs>
```

## pandoc extension

+---------------------+----------+
| Property            | Earth    |
+=============+=======+==========+
|             | min   | -89.2 °C |
| Temperature +-------+----------+
| 1961-1990   | mean  | 14 °C    |
|             +-------+----------+
|             | max   | 56.7 °C  |
+-------------+-------+----------+


# My Documentation


<table class="custom-table">
  <thead>
    <tr>
      <th>Header 1</th>
      <th>Header 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Row 1, Cell 1</td>
      <td>Row 1, Cell 2</td>
    </tr>
    <tr>
      <td>Row 2, Cell 1</td>
      <td>Row 2, Cell 2</td>
    </tr>
  </tbody>
</table>

## 测试eval-rst

这里的内容显示在网页。

```eval-rst
这里的内容不显示在网页。
```

## html-to-latex代码块

```{html-to-latex}
<table>
    <thead>
        <tr>
            <th>姓名</th>
            <th>年龄</th>
            <th>城市</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>张三</td>
            <td>28</td>
            <td>北京</td>
        </tr>
        <tr>
            <td>李四</td>
            <td>34</td>
            <td>上海</td>
        </tr>
        <tr>
            <td>王五</td>
            <td>22</td>
            <td>广州</td>
        </tr>
    </tbody>
</table>
```

## 跨行跨列

```{html-to-latex}
<table border="1" cellpadding="10" cellspacing="0">
    <thead>
        <tr>
            <th>姓名</th>
            <th>年龄</th>
            <th colspan="2">住址</th> <!-- 合并两列 -->
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>张三</td>
            <td>28</td>
            <td>北京市</td>
            <td>海淀区</td>
        </tr>
        <tr>
            <td>李四</td>
            <td rowspan="2">34</td> <!-- 合并两行 -->
            <td>上海市</td>
            <td>浦东新区</td>
        </tr>
        <tr>
            <td>广州市</td>
            <td>天河区</td>
        </tr>
    </tbody>
</table>
```

## custom table

自定义宽度表格示例1

```{table}
:widths: 6 1 1
:class: longtable
```
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| row11   | row12   | row13 |
| row21   | row22   | row23 |

示例结束。

自定义宽度表格示例2

```{table}
:widths: 3 4 4
:class: longtable
```
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| The `cd` command changes the directory you're working with. In order to work with your newly created Docusaurus site, you'll need to navigate the terminal there.   | The `npm run start` command builds your website locally and serves it through a development server, ready for you to view at http://localhost:3000/.   | row13 |
| row21   | The `npm run start` command builds your website locally and serves it through a development server, ready for you to view at http://localhost:3000/.   | row23 |

示例结束。

自定义宽度表格示例2

```{table}
:widths: 5 4 1
:class: longtable
```
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| The `cd` command changes the directory you're working with. In order to work with your newly created Docusaurus site, you'll need to navigate the terminal there.   | The `npm run start` command builds your website locally and serves it through a development server, ready for you to view at http://localhost:3000/.   | row13 |
| row21   | The `npm run start` command builds your website locally and serves it through a development server, ready for you to view at http://localhost:3000/.   | row23 |

示例结束。