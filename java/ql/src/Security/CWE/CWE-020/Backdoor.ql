import java

// Define a class to represent a potentially vulnerable query
class VulnerableQuery extends SQLQuery {
  VulnerableQuery() { this.getAst().hasArgument(0) and this.getAst().getArgument(0).getType().inherits("java.lang.String") }

  // Identify if the query uses user input to form part of the query string
  // Returns true if it does
  predicate hasUserInput() {
    exists(MethodAccess methodAccess |
      methodAccess.getMethod().getName() = "getParameter" and
      methodAccess.getArgument(0).getType().getName() = "java.lang.String" and
      methodAccess.getArgument(0).toString() = "userInput" and
      this.getAst().hasDescendant(methodAccess)
    )
  }
}

// Define a class to represent a potentially vulnerable method
class VulnerableMethod extends Method {
  VulnerableMethod() { this.hasParameterOfType("java.lang.String[]") }

  // Identify if the method has a vulnerable query
  // Returns true if it does
  predicate hasVulnerableQuery() {
    exists(VulnerableQuery query | 
      this.getAST().hasDescendant(query.getAST()) and 
      query.hasUserInput()
    )
  }
}

// Find all methods that have a vulnerable query
from VulnerableMethod method
where method.hasVulnerableQuery()
select method
