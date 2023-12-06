/**
 * @name Use of a weak cryptographic algorithm
 * @description Using weak cryptographic algorithms can allow an attacker to compromise security.
 * @kind path-problem
 * @problem.severity error
 * @id go/weak-crypto-algorithm
 * @tags security
 *       experimental
 *       external/cwe/cwe-327
 *       external/cwe/cwe-328
 */

import go
import WeakCryptoAlgorithmCustomizations
import WeakCryptoAlgorithm::Flow::PathGraph

from WeakCryptoAlgorithm::Flow::PathNode source, WeakCryptoAlgorithm::Flow::PathNode sink
where WeakCryptoAlgorithm::Flow::flowPath(source, sink)
select sink.getNode().asExpr().getFile().getAbsolutePath()+"$$"+sink.getNode().asExpr().getFile().getLocation().getStartLine(),sink.getNode(), source, sink, "$@ is used in a weak cryptographic algorithm.",
  source.getNode(), "Sensitive data"
