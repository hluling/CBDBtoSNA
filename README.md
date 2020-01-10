# CBDBtoSNA
Note by LH: The .py mentioned in the README main text refers to CBDBtoSNA_vx.xx.py
README draft revision date: 02/12/2019.
Translation finished with help from ChiCheng.
## 一、简介 / I. Introduction：
**CBDBtoSNA.py** 是一个将**中国历代人物传记资料库** ([**China Biographical Database**](https://projects.iq.harvard.edu/cbdb)) 中的人物关系网络转换成:
- [**GEXF** (Graph Exchange XML Format)]( https://gephi.org/gexf/format/) 格式
- 或 [**GraphML**](http://graphml.graphdrawing.org/) 格式

的**Python 3**程序。GEXF 和 GraphML 格式文件可用于 [**Gephi**](http://graphml.graphdrawing.org/) 中的网络关系可视化。

**CBDBtoSNA.py** is a **Python 3** script that transforms the social relations data contained in the [**CBDB** (**China Biographical Database**)](https://projects.iq.harvard.edu/cbdb) into either: 
- a [**GEXF** (Graph Exchange XML Format)](https://gephi.org/gexf/format/) file
- or a [**GraphML**](http://graphml.graphdrawing.org/) file

that can be used to visualize the data (e.g., in [**Gephi**](https://gephi.org)).

## 二、输入文件 / II. Input File：
a_cbdb_data.xml
- 请根据实际情况修改输入文件名
   Please change filename accordingly
- 此输入文件须与CBDBtoSNA.py在同一文件夹中
   An input file and CBDBtoSNA.py should be in the same folder.

## 三、输出文件 / III. Output File：
xxxxx.gexf **或/or** xxxxx.graphml

## 四、使用前 / IV. Prerequisites：
用户端设备须有 Python 3。
另外，用户须安装 Python 工具库－[lxml](https://lxml.de/)。

User's computer must have Python 3 installed.
In addition, user must install the Python library—[lxml](https://lxml.de/).

## 五、使用 / V. How to Run the Script：
用户可在命令行界面（Command-Line Interface）中运行 CBDBtoSNA.py。
输入文件 (xxxxx.xml) 之路径须与 CBDBtoSNA.py 之路径相同。
输出文件将在同一个路径中。

Users can run CBDBtoSNA.py from a command-line interface.
The path of the input file (xxxxx.xml) must be the same as the path of CBDBtoSNA.py.
The output file will be in the same path.



## 六、人物范围选取 / VI.  Selectors：
由于资料库包含历代人物近四十万，且 Gephi 中所能处理的节点数与关系数有限，用户须根据以下三类参数来设定所取人物范围：
- 年份
- 性别
- 人物编号

参数设定只针对于 CBDB 中某个人物（即源 XML 中某个 \<Person>,见附录三）。

   1. 年份：
    用户可通过设定两个或一个年份来定义一个年份范围。
    如：
    -- 两个年份：－202（－代表公元前）和 9 所定义的年份范围是公元前202年（含）至公元9年（含）。
            `CBDBtoSNA.py a_cbdb_data.xml gexf -f -202 -t 9`  选取出生/死亡/指数年份在公元前202年（含）与公元9年（含）之间的人物之人物关系。
    -- 一个年份：－202 所定义的年份范围可以是公元前202年（含）及之前或公元前202年（含）及之后。
`CBDBtoSNA.py a_cbdb_data.xml -t -202`  选取出生/死亡/指数年份在公元前202年（含）及之前的人物之人物关系。
`CBDBtoSNA.py a_cbdb_data.xml -f -202`  选取出生/死亡/指数年份在公元前202年（含）及之后的人物之人物关系。
    -- 注：年份参数可与性别参数（见下）搭配使用，但不可与人物编号（见下）搭配使用。

 2. 性别：
    参数值：1为男性，2为女性 (ISO/IEC 5218)
    `CBDBtoSNA.py a_cbdb_data.xml gexf -f -202 -t 9 －g 2`  选取出生/死亡/指数年份在公元前202年（含）与公元9年（含）之间的女性人物之人物关系。
   --  注1：性别参数可与年份参数搭配使用，但不可与人物编号（见下）搭配使用。
    -- 注2：为避免输出文件过大，建议勿仅使用性别参数，性别应搭配年份使用。

3. 个人网络（根据 CBDB 人物编号）：
    用户可输入至多十个（至少一个）人物编号来选取人物。
    用户可通过[CBDB网上查询系统](http://db1.ihp.sinica.edu.tw/cbdbc/ttsweb?@0:0:1:cbdbkm)获取人物编号。
    `CBDBtoSNA.py a_cbdb_data.xml graphml -pid 1762 38653`  选取CBDB人物编号为1762及38653的两个人物之人物关系。
    -- 注1：人物编号不可与性别或年份参数搭配使用。
    -- 注2：如使用人物编号，对于其中某人物（A），用户可选择将A之网络关系目标（B）之目标（C）一并加入到网络中，此为两个延伸度(Degree of 2)。用户还可选择将A之网络关系目标（B）之目标（C）之目标（D）一并加入到网络中，此为三个延伸度(Degree of 3)。延伸度为正整数，预设值为1，最大值为3。

As the complete CDBD is too large to be displayed efficiently, users are advised to select a subset of the data using the following parameters:
- date
- gender
- Ego-Networks (based on Person IDs)

The parameter settings are only for a person in the CBDB (i.e., a \<Person> in the source XML, see Appendix III).

 1. Year Date (-from & -to)：
The user can define a range of years.
   
    -- Using both -from and -to : 
    -f -202 (- for BC) and -t 9 defines a range of years from 202 BCE (inclusive) to 9 CE (inclusive).
`CBDBtoSNA.py a_cbdb_data.xml gexf -f -202 -t 9`  selects all relational information on people with birth/death/index years between -202 BCE (inclusive) and 9 CE (inclusive).
           
    -- Using only one date parameter:     
    -t -202 = 202 BCE (inclusive) and before
`CBDBtoSNA.py a_cbdb_data.xml graphml -t -202`  selects all relational information on people with birth/death/index years before -202 BCE (inclusive).
	-f -202 = 202 BCE (inclusive) and after
`CBDBtoSNA.py a_cbdb_data.xml gexf -f -202`  selects all relational information on people with birth/death/index years after -202 BCE (inclusive).

    -- Note: The date parameters can be used with gender parameter, but not with ego-network (i.e., Person ID) parameter.

 2. Gender:
    Parameter values: 1 = male, 2 = female (ISO/IEC 5218)
    `CBDBtoSNA.py a_cbdb_data.xml gexf -f -202 -t 9 －g 2`  selects all relational information on people who are female with birth/death/index years between -202 BCE and 9 CE (inclusive).
  -- Note 1: The gender parameter can be used with the year parameter, but not with the person number (see below).
  -- Note 2: In order to avoid large output files,it is advisable to use -gender with the date parameters -from and -to.
  
   3. Ego-Networks (based on Person IDs)：
    Users can enter between 1 and 10 Person IDs to select CBDB entries.
    Users can retrieve Person IDs from [CBDB's online query website](http://db1.ihp.sinica.edu.tw/cbdbc/ttsweb?@0:0:1:cbdbkm).
    `CBDBtoSNA.py a_cbdb_data.xml graphml -pid 1762 38653`  selects all relational information on people whose CBDB Person IDs are 1762 and 38653.
    -- Note 1: IDs cannot be used with gender or date parameter.
    -- Note 2:  Degree parameter: Users can specify to expand the ego-networks to the 2nd and 3rd degree by setting the degree parameter (-d / -degree) to 2 or 3. 



## 七、命令行中参数设定（详情见上文四，范例见下文八）/ VII. Command line Parameters (for details, see Section IV above; for examples,  see Section VIII below):

    Argparse 预设参数(Default argument)：
    -h      --help          显示帮助信息（英文）
						    Show help information (in English)。

    Argparse 必选参数(Positional arguments; Required)
    xmlInput                输入文件名 （xxxxx.xml; 区分大小写）
						    Input xml file name（xxxxx.xml; Case sensitive）
    outputFormat            输出格式名（gexf 或 graphml; 不区分大小写）
						    Output format (Values: gexf or graphml; NOT case sensitive）
    
    Argparse 可选参数(Optional arguments)
    -f      --fromY         指定起始年份（含）。如为公元前年份，在数字前加'-'。
						    Specify starting year (inclusive). For BCE, prepend '-'.
    -t      --toY           指定终止年份（含）。如为公元前年份，在数字前加'-'。
						    Specify ending year (inclusive). For BCE, prepend '-'.
    -g      --gender        指定性别：1为男性，2为女性。
						    Specify gender. 1 for male, 2 for female.
    -pid    --personID      指定CBDB中人物编号。请勿在某个编号前加零。两个或以上编号须以空格间隔。至多十个，至少一个。
						    Specify CBDB Person ID(s). Please do not prepend zero to an ID.
							Separate two IDs by a space. There should be at least one Person ID (no more than ten).
    -d      --degree        指定个人网络之延伸度。正整数，预设值为1，最大值为3。
						    Specify degree of ego-network.
						    The value should be a positive integer (default is one, maximum is 3).

    Argparse 详情/details: https://docs.python.org/3.6/library/argparse.html#module-argparse

## 八、命令行中参数设定范例 / VIII. Examples：

    1. 两个年份 / Select all persons between 202 BCE and 9 CE, return a .gexf file：
    CBDBtoSNA.py a_cbdb_data.xml gexf -f -202 -t 9
        
    2. 两个年份及女性 / Select all women between 202 BCE and 9 CE, return a .gexf file：
    CBDBtoSNA.py a_cbdb_data.xml gexf -f -202 -t 9 －g 2
        
    3. 一个年份（此年份（含）及之前）/ Select all persons before 202 BCE (inclusive), return a .graphml file：
    CBDBtoSNA.py a_cbdb_data.xml graphml -t -202
        
    4. 一个年份（此年份（含）及之后）及男性 / Select all men after 9 CE (inclusive), return a .graphml file：
    CBDBtoSNA.py a_cbdb_data.xml graphml -f 9 -g 1
  
    5. 两个人物编号（王安石、吴氏）/ Select the ego-networks of two persons (Wang Anshi and Wu Shi), return a .gexf file：
    CBDBtoSNA.py a_cbdb_data.xml gexf -pid 1762 38653

    6. 三个人物编号及两个延伸度 / Select three persons returning a 2-degree ego network for each, return a .graphml file:
    CBDBtoSNA.py a_cbdb_data.xml graphml -pid 128931 220217 34919 -d 2

----------------------------------------------------------------------
## 附录 / Appendices

### 一、GEXF 与 GraphML 中的网络节点 / I. Node in GEXF and GraphML
    1. 一节点对应一人物
    2. 节点编号形式：
       “n” ＋ CBDB中人物编号 
    3. 节点属性：
        a. 拼音名（如此人在CBDB中，则默认为Gephi可视化中的节点标签，node label）
        b. 中文名（对应GEXF/GraphML之节点属性n@chName;如此人不在CBDB中，则为Gephi可视化中节点标签）
        c. 出生年份（如有；对应GEXF/GraphML之节点属性n@birthY）
        d. 死亡年份（如有；对应GEXF/GraphML之节点属性n@deathY）
        e. 指数年份（如有；对应GEXF/GraphML之节点属性n@indexYear）
        f. 朝代（如有；对应GEXF/GraphML之节点属性n@dynasty）
        
    1. One node represents one person.
    2. Node identifier's format：
       “n” ＋ CBDB Person ID 
    3. Node attributes：
        a. Pinyin name（If a person exists in CBDB as a <Person> element，the Pinyin name is the node label of that person in Gephi）
        b. Chinese name（corresponding to the node attribute name, n@chName, in GEXF/GraphML; If a person does not exist in CBDB as a <Person> element，the Chinese name is the node label of that person in Gephi）
        c. Birth year（If available: corresponding to the node attribute name, n@birthY, in GEXF/GraphML）
        d. Death year（If available: corresponding to the node attribute name, n@deathY, in GEXF/GraphML）
        e. Index year（If available: corresponding to the node attribute name, n@indexY, in GEXF/GraphML）
        f. Dynasty（If available: corresponding to the node attribute name, n@dynasty, in GEXF/GraphML）

### 二、GEXF / GraphML 中的网络关系 / II. Edge in GEXF / GraphML
    1. 某关系中两个节点的编号对应上述节点编号（附录一）。
    2. 关系无方向性。
    3. 关系编号形式：
       “e” ＋ 自然数
    4. 关系属性：
        a. 关系性质：亲属关系或社会关系 (对应GEXF/GraphML之关系属性e@edgeType)
        b. 关系内容 (对应GEXF/GraphML之关系属性e@label)
        c. 资料来源 (对应GEXF/GraphML之关系属性e@bibl)
    
    1. Node identifiers in edge follow the node identifier format specified above (see Appendix I).
    2. Edge is undirectional.
    3. Edge identifier format:
        "e" + natural number
    4. Edge attributes:
         a. Edge type: 'Kinship' or 'Association' (corresponding to the edge attribute name, e@edgeType, in GEXF/GraphML)
         b. Edge label: Nature of a relationship (corresponding to the edge attribute name, e@label, in GEXF/GraphML)
         c. Source of information (corresponding to the edge attribute name, e@bibl, in GEXF/GraphML)

### 三、关于年份与性别设定范围与输出文件中人物范围 / III. The user-specified range of persons and the range of persons in output
    由于参数设定只针对于CBDB中某个人物（即源XML中某个<Person>），若视人物(<Person>)为某关系中的X，则此关系中的Y有可能在所设年份及性别范围之外。
    
    Parameter setting applies only to the attributes found in <Person> elements in a CBDB XML input file. That is, the source of an edge always comes from <Person> and is always within a user-specified range of date and/or gender. However, the target of an edge may be outside the user-specified range.

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTkwNTczMzg4XX0=
-->
