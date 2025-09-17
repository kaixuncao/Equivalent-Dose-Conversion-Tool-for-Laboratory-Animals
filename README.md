# 不同实验动物依据体表面积的等效剂量转换便捷计算工具（Equivalent-Dose-Conversion-Tool-for-Laboratory-Animals）

这是一个python编写并直接打包成exe的实验动物等效剂量转化工具，数据来源于FDA指南 http://www.fda.gov/downloads/Drugs/.../Guidances/UCM078932.pdf
该软件提供了如下的内容，并且可以中英文切换，以及窗口缩放（但是有最小值）。

<div align="center">
  
<img width="702" height="482" alt="image" src="https://github.com/user-attachments/assets/8d575b5b-e924-4137-a68f-e98c6f66cadc" />

</div>

具体的转换公式为：动物A剂量(mg/kg) = 动物B剂量(mg/kg) ×动物B的Km系数/动物A的Km系数 例如，依据体表面积折算法，将某药物用于小鼠的剂量22.6mg/kg换算成大鼠的剂量，需要将22.6mg/kg乘以小鼠的Km系数(3)，再除以大鼠的Km系数(6)，得到此药物用于大鼠的等效剂量为11.3mg/kg。


<div align="center">
  大鼠剂量(mg/kg) =小鼠剂量(22.6mg/kg) ×小鼠的Km系数(3)/ 大鼠的Km系数(6)=11.3 mg/kg
</div>
具体系数如下：

<p align="center"><font face="黑体" size=2.>表1 不同实验动物依据体表面积的等效剂量转换表</font></p>

<div align="center">
  
|   | 小鼠 | 大鼠 | 兔 | 豚鼠 | 仓鼠 | 狗 |
|---|---|---|---|---|---|---|
| 重量 (kg) | 0.02 | 0.15 | 0.15 | 0.4 | 0.08 | 10 |
| 体表面积 (m²) | 0.007 | 0.025 | 0.15 | 0.05 | 0.05 | 0.5 |
| Km 系数 | 3 | 6 | 12 | 8 | 5 | 20 |

</div>

该软件使用了ttkbootstrap作为美化模块，请先运行

    python dose_converter.py
    
因此MAC和Linux用户（Windows同理，但是我更推荐直接打包好的，不放心你也可以通过pyinstaller再打包一次）直接运行：

    pip install ttkbootstrap

如果有什么其他问题请带图给我看看，我会尽量修复它的，谢谢。
