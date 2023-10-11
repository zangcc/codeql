import javascript

//数组的值里面有localhost，所以检测所有的数组的值是否包含localhost，或者http://localhost
from ArrayExpr array, StringLiteral str
where
str = array.getAnElement() and
(str.getValue().matches("%localhost%") or str.getValue().matches("%http://localhost%"))

select array.getLocation().getFile().getAbsolutePath() +"$$" + array.getLocation().getStartLine()+"  数组值中存在localhost,请手工检查是否敏感: "+array

