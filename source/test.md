# test

## test1

测试是否能识别markdown文件。

## test2

测试是否能识别markdown文件。

## html表格


## 示例表格

Here is an HTML table:

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
    <table style="width: 50%; border-collapse: collapse;">
        <tr>
            <th style="text-align: center; width: 50%;border: 1px solid black;">编号</th>
            <th style="text-align: center; width: 50%;border: 1px solid black;" colspan="2">姓名</th>
        </tr>
        <tr>
            <td style="width: 50%;border: 1px solid black;">1</td>
            <td style="text-align: left; width: 50%;border: 1px solid black;">张三</td>
            <td style="text-align: right;width: 50%; border: 1px solid black;">25</td>
        </tr>
        <tr>
            <td style="border: 1px solid black;" rowspan="2">2</td>
            <td style="text-align: left; border: 1px solid black;">李四</td>
            <td style="text-align: right; border: 1px solid black;">30</td>
        </tr>
        <tr>
            <td style="text-align: left; border: 1px solid black;" colspan="2">王五</td>
        </tr>
        <tr>
            <td style="border: 1px solid black;" colspan="3">备注：以上是示例数据</td>
        </tr>
    </table>

```