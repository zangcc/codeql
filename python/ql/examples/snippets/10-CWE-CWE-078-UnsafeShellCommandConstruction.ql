/**
 * @name Unsafe shell command constructed from library input
 * @description Using externally controlled strings in a command line may allow a malicious
 *              user to change the meaning of the command.
 * @kind path-problem
 * @problem.severity error
 * @security-severity 6.3
 * @precision medium
 * @id py/shell-command-constructed-from-input
 * @tags correctness
 *       security
 *       external/cwe/cwe-078
 *       external/cwe/cwe-088
 *       external/cwe/cwe-073
 */

import python
import semmle.python.security.dataflow.UnsafeShellCommandConstructionQuery
import DataFlow::PathGraph

from Configuration config, DataFlow::PathNode source, DataFlow::PathNode sink, Sink sinkNode
where
  config.hasFlowPath(source, sink) and
  sinkNode = sink.getNode()
select sink.getNode().getLocation().getFile().getAbsolutePath()+"$$"+sink.getNode().getLocation().getStartLine(),sinkNode.getStringConstruction(), source, sink,
  "This " + sinkNode.describe() + " which depends on $@ is later used in a $@.", source.getNode(),
  "library input", sinkNode.getCommandExecution(), "shell command"
