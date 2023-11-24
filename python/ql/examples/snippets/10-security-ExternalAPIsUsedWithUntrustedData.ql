/**
 * @name Frequency counts for external APIs that are used with untrusted data
 * @description This reports the external APIs that are used with untrusted data, along with how
 *              frequently the API is called, and how many unique sources of untrusted data flow
 *              to it.
 * @id py/count-untrusted-data-external-api
 * @kind table
 * @tags security external/cwe/cwe-20
 */

import python
import ExternalAPIs

from ExternalApiUsedWithUntrustedData externalApi
select e, e.getLocation().getFile().getAbsolutePath()+"$$"+e.getLocation().getStartLine()xternalApi, count(externalApi.getUntrustedDataNode()) as numberOfUses,
  externalApi.getNumberOfUntrustedSources() as numberOfUntrustedSources order by
    numberOfUntrustedSources desc
