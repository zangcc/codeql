/**
 * @name 系统对传入的参数没有做过滤处理或者只做了简单过滤，参数即参与下面的流程，可能会造成漏洞或者系统异常告警
 * @description 可能存在漏洞的java代码示例
 * 此处code为验证码，此处没有对用户传入的验证码做任何校验
 * public class VerifyCodeRequest<T> {
    @NotNull
    private T code;
 }
 *              
 * @author ba1ma0@Safeheron
 */



import java
from Method m, Parameter p,string fullTypeName,Class cls,Field filed,string loc,string loc1
where m.hasAnnotation("org.springframework.web.bind.annotation","PostMapping")
  and p = m.getParameter(0)
  and fullTypeName = p.getType().toString()  
  and cls.getName().toString() = getClassName(fullTypeName)
  and filed.getDeclaringType().toString() = cls.getName().toString() 
  and filed.toString()  = filed.getAnAssignedValue().toString() //private只能是这种格式 private String code;
  and loc  = filed.getLocation().getFile().getAbsolutePath() + "$$" + filed.getLocation().getStartLine()
  and loc1 = m.getLocation().getFile().getAbsolutePath() + "$$" + m.getLocation().getStartLine()
  and onlyHasSpecialAnotaion(filed.getAnAnnotation())= "True"
select "传入参数点: "+loc1,"传入的参数: "+filed,"系统只做了 NotBlank, NotNull,Valid, NotEmpty简单注释过滤处理",loc



bindingset[fullTypeName]
string getClassName(string fullTypeName) {
  countChar(fullTypeName,">")=0 and result = fullTypeName or
  countChar(fullTypeName,">") >0 and result = getLastTypeName(fullTypeName,fullTypeName.splitAt("<",countChar(fullTypeName, ">")).replaceAll(">", ""))
}



bindingset[str,flag]
int countChar(string str, string flag) {
  result = str.length() - str.replaceAll(flag.toString(), "").length()
}



bindingset[fullTypeName,lastName]
string getLastTypeName(string fullTypeName,string  lastName) {

lastName  = ["Void","Integer","String"] and result = fullTypeName.splitAt("<",countChar(fullTypeName, ">")-1).replaceAll(">", "") or
not lastName  = ["Void","Integer","String"] and result = fullTypeName.splitAt("<",countChar(fullTypeName, ">")).replaceAll(">", "")
   
}

bindingset[a]
string onlyHasSpecialAnotaion(Annotation a) {
  a.getType().hasName(["NotBlank", "NotNull", "Valid", "NotEmpty"])
  and not exists(Annotation b | b.getAnnotatedElement() = a.getAnnotatedElement() and not b.getType().hasName(["NotBlank", "NotNull", "Valid", "NotEmpty"]))
  and result = "True"
}





