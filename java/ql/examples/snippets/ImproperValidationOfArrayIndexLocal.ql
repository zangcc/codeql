/**
 * @name Improper validation of local user-provided array index
 * @description Using local user input as an index to an array, without
 *              proper validation, can lead to index out of bound exceptions.
 * @kind path-problem
 * @problem.severity recommendation
 * @security-severity 8.8
 * @precision medium
 * @id java/improper-validation-of-array-index-local
 * @tags security
 *       external/cwe/cwe-129
 */

import java
import semmle.code.java.security.internal.ArraySizing
import semmle.code.java.security.ImproperValidationOfArrayIndexLocalQuery
import ImproperValidationOfArrayIndexLocalFlow::PathGraph

from
  ImproperValidationOfArrayIndexLocalFlow::PathNode source,
  ImproperValidationOfArrayIndexLocalFlow::PathNode sink, CheckableArrayAccess arrayAccess
where
  arrayAccess.canThrowOutOfBounds(sink.getNode().asExpr()) and
  ImproperValidationOfArrayIndexLocalFlow::flowPath(source, sink)
select arrayAccess.getLocation().getFile().getAbsolutePath()+"$$"+arrayAccess.getLocation().getStartLine() ,arrayAccess.getIndexExpr(), source, sink,
  "This index depends on a $@ which can cause an ArrayIndexOutOfBoundsException.", source.getNode(),
  "user-provided value"
