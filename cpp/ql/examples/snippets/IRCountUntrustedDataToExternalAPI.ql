/**
 * @name Frequency counts for external APIs that are used with untrusted data
 * @description This reports the external APIs that are used with untrusted data, along with how
 *              frequently the API is called, and how many unique sources of untrusted data flow
 *              to it.
 * @id cpp/count-untrusted-data-external-api-ir
 * @kind table
 * @tags security external/cwe/cwe-20
 */

import cpp
import ir.ExternalAPIs

from ExternalApiUsedWithUntrustedData externalApi
select externalApi.getLocation().getFile().getAbsolutePath()+"$$"+externalApi.getLocation().getStartLine() ,externalApi, count(externalApi.getUntrustedDataNode()) as numberOfUses,
  externalApi.getNumberOfUntrustedSources() as numberOfUntrustedSources order by
    numberOfUntrustedSources desc