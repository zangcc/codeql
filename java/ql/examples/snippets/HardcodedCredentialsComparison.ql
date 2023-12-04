/**
 * @name Hard-coded credential comparison
 * @description Comparing a parameter to a hard-coded credential may compromise security.
 * @kind problem
 * @problem.severity error
 * @security-severity 9.8
 * @precision low
 * @id java/hardcoded-credential-comparison
 * @tags security
 *       external/cwe/cwe-798
 */

import java
import semmle.code.java.security.HardcodedCredentialsComparison

from EqualsAccess sink, HardcodedExpr source, PasswordVariable p
where isHardcodedCredentialsComparison(sink, source, p)
select source.getNode().getLocation().getFile().getAbsolutePath()+"$$"+source.getNode().getLocation().getStartLine(),source.getNode().getLocation().getFile().getAbsolutePath()+"$$"+source.getNode().getLocation().getStartLine() ,source, "Hard-coded value is $@ with password variable $@.", sink, "compared", p, p.getName()
