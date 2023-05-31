// 查询6：检测Java中可能存在后门的加密算法选择
import java

from MethodAccess ma, StringLiteral sl
where ma.getMethod().hasName("getInstance") and 
  ma.getMethod().getDeclaringType() instanceof TypeCipher and 
  ma.getArgument(0) = sl and 
  not (sl.getValue() = "AES" or sl.getValue() = "RSA" or sl.getValue() = "DES")
select ma, "Possible backdoor encryption algorithm selection."