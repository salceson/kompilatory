package simplifier

import AST._

// to implement
// avoid one huge match of cases
// take into account non-greedy strategies to resolve cases with power laws
object Simplifier {

  def simplify(node: Node): Node = node match {
    case Unary("not", expr) => expr match {
      case BinExpr("==", left, right) => BinExpr("!=", simplify(left), simplify(right))
      case BinExpr("!=", left, right) => BinExpr("==", simplify(left), simplify(right))
      case BinExpr("<=", left, right) => BinExpr(">",  simplify(left), simplify(right))
      case BinExpr(">=", left, right) => BinExpr("<",  simplify(left), simplify(right))
      case BinExpr("<", left, right)  => BinExpr(">=", simplify(left), simplify(right))
      case BinExpr(">", left, right)  => BinExpr("<=", simplify(left), simplify(right))

      case TrueConst()                => FalseConst()
      case FalseConst()               => TrueConst()

      case Unary("not", expr2)        => simplify(expr2) // double negation

      case expr2                      => Unary("not", simplify(expr2))
    }

    case Unary("-", expr) => expr match {
      case Unary("-", expr2) => simplify(expr2)
      case expr2             => Unary("-", simplify(expr2))
    }

    case BinExpr("+", left, right)    => (left, right) match {
      case (Variable(x), Variable(y)) if x == y => IntNum(0) // TODO czy tu int?
      case (exprL, exprR) => BinExpr("+", simplify(exprL), simplify(exprR))
    }

    case n => n
  }

}
