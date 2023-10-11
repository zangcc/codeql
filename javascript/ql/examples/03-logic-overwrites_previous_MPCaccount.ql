import javascript

//定义一个函数,用来判断KeyGenFlow.ts文件内的keyGenApproval函数的作用域（成员变量）内是否存在existWallet变量
predicate isexistWallet() {

    not exists(Function f,VarDecl v|f.getFile().getBaseName() = "KeyGenFlow.ts" and
    f.getName() = "keyGenApproval" and 
    v.getEnclosingFunction() = f and 
    v.getName() = "existWallet")
    }

//声明一个函数f
from Function f

where isexistWallet() and //当isexistWallet()函数为true，也就是上述函数的条件不满足时（not exists）
 f.getFile().getBaseName() = "KeyGenFlow.ts" and //在KeyGenFlow.ts文件内查找
 f.getName() = "keyGenApproval" //在KeyGenFlow.ts文件内定位到关键函数keyGenApproval

 //如果函数内的条件不成立，则说明没有声明existWallet变量来进行逻辑判断，漏洞存在。
 select f.getLocation().getFile().getAbsolutePath() +"$$" + f.getLocation().getStartLine()+"  疑似存在密钥生成覆盖先前的MPC帐户: "+f


