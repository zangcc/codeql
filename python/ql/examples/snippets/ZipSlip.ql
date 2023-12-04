/**
 * @name Arbitrary file access during archive extraction ("Zip Slip")
 * @description Extracting files from a malicious ZIP file, or similar type of archive, without
 *              validating that the destination file path is within the destination directory
 *              can allow an attacker to unexpectedly gain access to resources.
 * @kind path-problem
 * @id py/zipslip
 * @problem.severity error
 * @security-severity 7.5
 * @precision high
 * @tags security
 *       experimental
 *       external/cwe/cwe-022
 */

import python
import experimental.semmle.python.security.ZipSlip
import DataFlow::PathGraph

from ZipSlipConfig config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select source.getNode().getLocation().getFile().getAbsolutePath()+"$$"+source.getNode().getLocation().getStartLine(),source.getNode(), source, sink,
  "This unsanitized archive entry, which may contain '..', is used in a $@.", sink.getNode(),
  "file system operation"
