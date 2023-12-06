/**
 * @name Command Injection into Runtime.exec() with dangerous command
 * @description High sensitvity and precision version of java/command-line-injection, designed to find more cases of command injection in rare cases that the default query does not find
 * @kind path-problem
 * @problem.severity error
 * @security-severity 6.1
 * @precision high
 * @id java/command-line-injection-extra-local
 * @tags security
 *       experimental
 *       local
 *       external/cwe/cwe-078
 */

import CommandInjectionRuntimeExec
import ExecUserFlow::PathGraph

class LocalSource extends Source instanceof LocalUserInput { }

from
  ExecUserFlow::PathNode source, ExecUserFlow::PathNode sink, DataFlow::Node sourceCmd,
  DataFlow::Node sinkCmd
where callIsTaintedByUserInputAndDangerousCommand(source, sink, sourceCmd, sinkCmd)
select sink.getNode().asExpr().getFile().getAbsolutePath()+"$$"+sink.getNode().asExpr().getFile().getLocation().getStartLine(),sink.getLocation().getFile().getAbsolutePath()+"$$"+sink.getLocation().getStartLine() ,sink, source, sink,
  "Call to dangerous java.lang.Runtime.exec() with command '$@' with arg from untrusted input '$@'",
  sourceCmd, sourceCmd.toString(), source.getNode(), source.toString()
