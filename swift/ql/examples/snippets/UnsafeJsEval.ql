/**
 * @name JavaScript Injection
 * @description Evaluating JavaScript code containing a substring from a remote source may lead to remote code execution.
 * @kind path-problem
 * @problem.severity warning
 * @security-severity 9.3
 * @precision medium
 * @id swift/unsafe-js-eval
 * @tags security
 *       external/cwe/cwe-094
 *       external/cwe/cwe-095
 *       external/cwe/cwe-749
 */

import swift
import codeql.swift.dataflow.DataFlow
import codeql.swift.security.UnsafeJsEvalQuery
import UnsafeJsEvalFlow::PathGraph

from
  UnsafeJsEvalFlow::PathNode sourceNode, UnsafeJsEvalFlow::PathNode sinkNode, UnsafeJsEvalSink sink
where
  UnsafeJsEvalFlow::flowPath(sourceNode, sinkNode) and
  sink = sinkNode.getNode()
select sink.getNode().asExpr().getFile().getAbsolutePath()+"$$"+sink.getNode().asExpr().getFile().getLocation().getStartLine() ,sink, sourceNode, sinkNode, "Evaluation of uncontrolled JavaScript from a remote source."
