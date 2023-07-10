/**
 * @name Untrusted data passed to external API
 * @description Data provided remotely is used in this external API without sanitization, which could be a security risk.
 * @id cpp/untrusted-data-to-external-api-ir
 * @kind path-problem
 * @precision low
 * @problem.severity error
 * @security-severity 7.8
 * @tags security external/cwe/cwe-20
 */

import cpp
import semmle.code.cpp.ir.dataflow.TaintTracking
import ir.ExternalAPIs
import semmle.code.cpp.security.FlowSources
import DataFlow::PathGraph

from UntrustedDataToExternalApiConfig config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink, source,sink.getNode().getLocation().getFile().getAbsolutePath()+"$$"+sink.getNode().getLocation().getStartLine(),
  "Call to " + sink.getNode().(ExternalApiDataNode).getExternalFunction().toString() +
    " with untrusted data from $@.", source, source.getNode().(RemoteFlowSource).getSourceType()
