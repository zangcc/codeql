// import cpp

// from GlobalVariable v,int count1,FunctionCall fc
// where   v.hasInitializer() 
//         and count1 = count(v.getInitializer()) 
//         and count1 =1
//         and v.getFile().getBaseName().regexpMatch("\\.cpp$")
// select v, "全局变量被初始化了两次,可能存在安全风险", count1,fc.getLocation().getFile().getAbsolutePath() + ":" + fc.getLocation().getStartLine().toString()



// import cpp

// from GlobalVariable v, VariableDeclarationEntry vde1, VariableDeclarationEntry vde2
// where
//   v.getADeclarationEntry() = vde1 and
//   v.getADeclarationEntry() = vde2 and
//   vde1 != vde2 and
//   vde1.getFile() = vde2.getFile() and
//   vde1.isDefinition() and
//   vde2.isDefinition()
// select v, "This global variable is initialized twice: once at " + vde1.getLocation().toString() + " and again at " + vde2.getLocation().toString()

import cpp

from GlobalVariable gv, Variable v
where
  gv.getName() = v.getName() and
  gv != v and
  gv.hasInitializer() and
  v.hasInitializer() and
  gv.getParentScope() != v.getParentScope()
select v,gv,"全局变量在函数内第二次被初始化了,可能存在安全风险" ,gv.getLocation().getFile().getAbsolutePath() + ":" + gv.getLocation().getStartLine().toString()+":"+v.getLocation().getStartLine().toString()