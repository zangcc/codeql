/**
 * @name Untrusted data passed to external API
 * @description Data provided remotely is used in this external API without sanitization, which could be a security risk.
 * @id js/untrusted-data-to-external-api
 * @kind path-problem
 * @precision low
 * @problem.severity error
 * @security-severity 7.8
 * @tags security external/cwe/cwe-20
 */

import javascript
import semmle.javascript.security.dataflow.ExternalAPIUsedWithUntrustedDataQuery
import DataFlow::PathGraph

from Configuration config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink.getNode().asExpr().getFile().getAbsolutePath()+"$$"+sink.getNode().asExpr().getFile().getLocation().getStartLine(),sink.getLocation().getFile().getAbsolutePath()+"$$"+sink.getLocation().getStartLine() ,sink, source, sink,
  "Call to " + sink.getNode().(Sink).getApiName() + " with untrusted data from $@.", source,
  source.toString()
