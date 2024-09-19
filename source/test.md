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