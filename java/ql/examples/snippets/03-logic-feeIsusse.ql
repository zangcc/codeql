// import java

// from MethodAccess ma, Method m,MethodAccess ma1, Method m1
// where ma.getMethod() = m
//   and m.getName().toString()="getCoinImplTag"
//   and ma.getQualifier().toString()="coinInfo"
// select ma ,ma.getCallee().getParameter(0),ma.getQualifier().toString(),"This method access compares coin's implementation tag with SUI's code."



import java

from MethodAccess ma, Method m
where ma.getMethod() = m and
  m.getName() = "getCode" and
  m.getQualifiedName()= "CoinImplTagEnum.UTXO" 
select ma, "This method access calls UTXO.getCode and its return value is used as the qualifier of Object.equals."
