package simplifier

import AST._
import math.pow

// to implement
// avoid one huge match of cases
// take into account non-greedy strategies to resolve cases with power laws
object Simplifier {

  def simplify(node: Node): Node = node match {
    // na samym poczatku musza byc patterny najbardziej szczegolowe, zeby te bardziej ogolne ich
    // nie "zjadly" :)

    // <ewaluacja wyrazen> -------------------------------------------------------------------------------
    // ewaluacja jest taka dluga, jesli chcemy pozwolic na domyslne casty intow na floaty w wyrazeniach
    // nie ma wiele lepszego sposobu na zrobienie tego krocej (tzn. jest, ale trzeba troche podrasowac AST i uzyc
    // ruskich trickow. Ain't nobody got time for that :)
    case BinExpr(op, IntNum(x), IntNum(y)) =>
      op match {
        case "+"  => IntNum(x + y)
        case "-"  => IntNum(x - y)
        case "*"  => IntNum(x * y)
        case "/"  => IntNum(x / y)
        case "%"  => IntNum(x % y)
        case "**" => IntNum(pow(x.toDouble, y.toDouble).asInstanceOf[Integer]) // dlaczego Integer? dobre pytanie!

        case "==" => if (x == y) TrueConst() else FalseConst()
        case "!=" => if (x != y) TrueConst() else FalseConst()
        case ">=" => if (x >= y) TrueConst() else FalseConst()
        case "<=" => if (x <= y) TrueConst() else FalseConst()
        case ">"  => if (x > y)  TrueConst() else FalseConst()
        case "<"  => if (x < y)  TrueConst() else FalseConst()
      }

    case BinExpr(op, FloatNum(x), FloatNum(y)) =>
      op match {
        case "+"  => FloatNum(x + y)
        case "-"  => FloatNum(x - y)
        case "*"  => FloatNum(x * y)
        case "/"  => FloatNum(x / y)
        case "%"  => FloatNum(x % y)
        case "**" => FloatNum(pow(x, y))

        case "==" => if (x == y) TrueConst() else FalseConst()
        case "!=" => if (x != y) TrueConst() else FalseConst()
        case ">=" => if (x >= y) TrueConst() else FalseConst()
        case "<=" => if (x <= y) TrueConst() else FalseConst()
        case ">"  => if (x > y)  TrueConst() else FalseConst()
        case "<"  => if (x < y)  TrueConst() else FalseConst()
      }

    case BinExpr(op, IntNum(x), FloatNum(y)) =>
      op match {
        case "+"  => FloatNum(x + y)
        case "-"  => FloatNum(x - y)
        case "*"  => FloatNum(x * y)
        case "/"  => FloatNum(x / y)
        case "%"  => FloatNum(x % y)
        case "**" => FloatNum(pow(x.toDouble, y))

        case "==" => if (x == y) TrueConst() else FalseConst()
        case "!=" => if (x != y) TrueConst() else FalseConst()
        case ">=" => if (x >= y) TrueConst() else FalseConst()
        case "<=" => if (x <= y) TrueConst() else FalseConst()
        case ">"  => if (x > y)  TrueConst() else FalseConst()
        case "<"  => if (x < y)  TrueConst() else FalseConst()
      }

    case BinExpr(op, FloatNum(x), IntNum(y)) =>
      op match {
        case "+"  => FloatNum(x + y)
        case "-"  => FloatNum(x - y)
        case "*"  => FloatNum(x * y)
        case "/"  => FloatNum(x / y)
        case "%"  => FloatNum(x % y)
        case "**" => FloatNum(pow(x, y.toDouble))

        case "==" => if (x == y) TrueConst() else FalseConst()
        case "!=" => if (x != y) TrueConst() else FalseConst()
        case ">=" => if (x >= y) TrueConst() else FalseConst()
        case "<=" => if (x <= y) TrueConst() else FalseConst()
        case ">"  => if (x > y)  TrueConst() else FalseConst()
        case "<"  => if (x < y)  TrueConst() else FalseConst()
      }

    case BinExpr("==", x, y) if x == y => TrueConst()
    case BinExpr(">=", x,y)  if x == y => TrueConst()
    case BinExpr("<=", x,y)  if x == y => TrueConst()
    case BinExpr("!=", x,y)  if x == y => FalseConst()
    case BinExpr("<", x,y)   if x == y => FalseConst()
    case BinExpr(">", x,y)   if x == y => FalseConst()
    case BinExpr("or", x ,y) if x == y => x
    case BinExpr("and", x,y) if x == y => x

    // </ewaluacja wyrazen> --------------------------------------------------------------------------

    case Unary("not", expr) => expr match {
      case BinExpr("==", left, right) => simplify(BinExpr("!=", left, right))
      case BinExpr("!=", left, right) => simplify(BinExpr("==", left, right))
      case BinExpr("<=", left, right) => simplify(BinExpr(">",  left, right))
      case BinExpr(">=", left, right) => simplify(BinExpr("<",  left, right))
      case BinExpr("<", left, right)  => simplify(BinExpr(">=", left, right))
      case BinExpr(">", left, right)  => simplify(BinExpr("<=", left, right))

      case TrueConst()                => FalseConst()
      case FalseConst()               => TrueConst()

      case Unary("not", expr2)        => simplify(expr2) // double negation

      case expr2                      => Unary("not", simplify(expr2))
    }

    case Unary("-", expr) => expr match {
      case Unary("-", expr2) => simplify(expr2)
        // tutaj jeszcze tak naprawde czesc ewaluacji, ale juz zeby nie bylo az takiej redundancji tych kejsow...
      case IntNum(x)         => IntNum(-x)
      case FloatNum(x)       => FloatNum(-x)
      case expr2             => Unary("-", simplify(expr2))
    }

    case BinExpr("-", left, right)    => (left, right) match {
      case (Variable(x), Variable(y)) if x == y => IntNum(0) // TODO czy tu int? --> jakis w kazdym razie numerek
      case (Variable(x), IntNum(n))   if n == 0 => Variable(x)
      case (Variable(x), FloatNum(n)) if n == 0 => Variable(x)
      case (FloatNum(n), Variable(x)) if n == 0 => Unary("-", Variable(x))
      case (IntNum(n), Variable(x))   if n == 0 => Unary("-", Variable(x))
      case (exprL, exprR)                       => BinExpr("-", simplify(exprL), simplify(exprR))
    }

    case BinExpr("+", left, right)    => (left, right) match {
      case (Unary("-", n1), n2)       if n1 == n2 => IntNum(0)
      case (Variable(x), IntNum(n))   if n == 0   => Variable(x)
      case (Variable(x), FloatNum(n)) if n == 0   => Variable(x)
      case (FloatNum(n), Variable(x)) if n == 0   => Variable(x)
      case (IntNum(n), Variable(x))   if n == 0   => Variable(x)
      case (exprL, exprR)                         => BinExpr("-", simplify(exprL), simplify(exprR))
    }

    case NodeList(list) => NodeList(list map simplify)
    case n => n
  }

}
