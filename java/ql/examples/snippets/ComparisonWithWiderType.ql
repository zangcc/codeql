/**
 * @name Comparison of narrow type with wide type in loop condition
 * @description Comparisons between types of different widths in a loop condition can cause the loop
 *              to behave unexpectedly.
 * @kind problem
 * @problem.severity warning
 * @security-severity 8.1
 * @precision medium
 * @id java/comparison-with-wider-type
 * @tags reliability
 *       security
 *       external/cwe/cwe-190
 *       external/cwe/cwe-197
 */

import java
import semmle.code.java.arithmetic.Overflow

int leftWidth(ComparisonExpr e) { result = e.getLeftOperand().getType().(NumType).getWidthRank() }

int rightWidth(ComparisonExpr e) { result = e.getRightOperand().getType().(NumType).getWidthRank() }

abstract class WideningComparison extends BinaryExpr instanceof ComparisonExpr {
  abstract Expr getNarrower();

  abstract Expr getWider();
}

class LTWideningComparison extends WideningComparison {
  LTWideningComparison() {
    (this instanceof LEExpr or this instanceof LTExpr) and
    leftWidth(this) < rightWidth(this)
  }

  override Expr getNarrower() { result = this.getLeftOperand() }

  override Expr getWider() { result = this.getRightOperand() }
}

class GTWideningComparison extends WideningComparison {
  GTWideningComparison() {
    (this instanceof GEExpr or this instanceof GTExpr) and
    leftWidth(this) > rightWidth(this)
  }

  override Expr getNarrower() { result = this.getRightOperand() }

  override Expr getWider() { result = this.getLeftOperand() }
}

from WideningComparison c, LoopStmt l
where
  not c.getAnOperand().isCompileTimeConstant() and
  l.getCondition().getAChildExpr*() = c
select c.getLocation().getFile().getAbsolutePath()+"$$"+c.getLocation().getStartLine() ,c,
  "Comparison between $@ of type " + c.getNarrower().getType().getName() + " and $@ of wider type " +
    c.getWider().getType().getName() + ".", c.getNarrower(), "expression", c.getWider(),
  "expression"
