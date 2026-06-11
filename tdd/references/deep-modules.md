# Deep Modules

来自 "A Philosophy of Software Design" 的判断框架：

Deep module = small interface + deep implementation。

```text
+---------------------+
|   Small Interface   |  Few methods, simple params
+---------------------+
|                     |
|  Deep              |
|  Implementation    |  Complex logic hidden
|                     |
+---------------------+
```

Shallow module = large interface + thin implementation，通常要避免。

```text
+---------------------------------+
|       Large Interface           |  Many methods, complex params
+---------------------------------+
|  Thin Implementation            |  Just passes through
+---------------------------------+
```

设计 interface 时询问：

- 能否减少 method 数量？
- 能否简化 parameters？
- 能否把 ordering、config、error handling 或 branching complexity 藏进 implementation？
- 删除这个 module 后，复杂度是消失了，还是只是散回 callers？
