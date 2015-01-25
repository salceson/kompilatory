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

    // konkatenacja tupli i list na samym poczatku (albowiem j.w.):
    case BinExpr("+", Tuple(l1), Tuple(l2)) => Tuple(l1 ++ l2)
    case BinExpr("+", ElemList(l1), ElemList(l2)) => ElemList(l1 ++ l2)

    // usuwanie duplikatow ze slownikow:
    case KeyDatumList(list) => KeyDatumList(list.foldLeft(Map.empty[Node, KeyDatum])(
      (_map, kd) => _map + (kd.key -> kd)
    ).toList.map(p => p._2))

    // usuwanie petli z falszywym warunkiem:
    case WhileInstr(cond, body) =>
      val sCond = simplify(cond)
      sCond match {
        case FalseConst() => EmptyInstr()
        case _            => WhileInstr(sCond, simplify(body))
      }

    case IfElseInstr(cond, left, right) =>
      val sCond = simplify(cond)
      sCond match {
        case TrueConst()  => simplify(left)
        case FalseConst() => simplify(right)
        case _            => IfElseInstr(sCond, simplify(left), simplify(right))
      }

    case IfInstr(cond, left) =>
      val sCond = simplify(cond)
      sCond match {
        case TrueConst()  => simplify(left)
        case FalseConst() => EmptyInstr()
        case _            => IfInstr(sCond, simplify(left))
      }

    case IfElseExpr(cond, left, right) =>
      val sCond = simplify(cond)
      sCond match {
        case TrueConst()  => simplify(left)
        case FalseConst() => simplify(right)
        case _            => IfElseExpr(sCond, simplify(left), simplify(right))
      }

    case Assignment(Variable(x), expr) => expr match {
      case Variable(y) if x == y => EmptyInstr()
      case _                     => Assignment(Variable(x), simplify(expr))
    }

    // <ewaluacja wyrazen> -------------------------------------------------------------------------------
    // ewaluacja jest taka dluga, jesli chcemy pozwolic na domyslne casty intow na floaty w wyrazeniach
    // nie ma wiele lepszego sposobu na zrobienie tego krocej (tzn. jest, ale trzeba troche podrasowac AST i uzyc
    // ruskich trickow. Ain't nobody got time for that :)

    case BinExpr(op, IntNum(x), IntNum(y)) =>
      op match {
        case "+" => IntNum(x + y)
        case "-" => IntNum(x - y)
        case "*" => IntNum(x * y)
        case "/" => IntNum(x / y)
        case "%" => IntNum(x % y)
        case "**" => IntNum(pow(x.toDouble, y.toDouble).toInt)

        case "==" => if (x == y) TrueConst() else FalseConst()
        case "!=" => if (x != y) TrueConst() else FalseConst()
        case ">=" => if (x >= y) TrueConst() else FalseConst()
        case "<=" => if (x <= y) TrueConst() else FalseConst()
        case ">" => if (x > y)   TrueConst() else FalseConst()
        case "<" => if (x < y)   TrueConst() else FalseConst()
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

    // <upraszczanie wyrazen unarnych> --------------------------------------------------------------
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

    // </upraszczanie wyrazen unarnych> --------------------------------------------------------------

    // <upraszczanie wyrazen binarnych typu x + 0> --------------------------------------------------------------

    case BinExpr("-", left, right)    => (left, right) match {
      case (exprL, exprR) if exprL == exprR => IntNum(0)
      case (expr, IntNum(n)) if n == 0  => simplify(expr)
      case (IntNum(n), expr) if n == 0  => simplify(Unary("-", simplify(expr)))
      case (expr, FloatNum(n)) if n == 0 => simplify(expr)
      case (FloatNum(n), expr) if n == 0 => simplify(Unary("-", simplify(expr)))
      // commutative properties:
      case (e@BinExpr("+", exprL, exprR), expr) =>
        if (exprL == expr) simplify(exprR)
        else if (exprR == expr) simplify(exprL)
        else BinExpr("-", simplify(e), simplify(expr))
      case (expr, e@BinExpr("+", exprL, exprR)) =>
        if (exprL == expr) simplify(Unary("-", exprR))
        else if (exprR == expr) simplify(Unary("-", exprL))
        else BinExpr("-", simplify(expr), simplify(e))

      case (exprL, exprR)      =>
        val sL = simplify(exprL)
        val sR = simplify(exprR)
        if (sL != exprL || sR != exprR) simplify(BinExpr("-", sL, sR)) else BinExpr("-", sL, sR)
    }

    case BinExpr("+", left, right)    => (left, right) match {
      case (expr, IntNum(n)) if n == 0  => simplify(expr)
      case (IntNum(n), expr) if n == 0  => simplify(expr)
      case (expr, FloatNum(n)) if n == 0 => simplify(expr)
      case (FloatNum(n), expr) if n == 0 => simplify(expr)
      case (Unary("-", exprU), expr) => simplify(BinExpr("-", expr, exprU))
      case (expr, Unary("-", exprU)) => simplify(BinExpr("-", expr, exprU))
      // commutative properties:
      case (e@BinExpr("-", exprL, exprR), expr) =>
        if (exprR == expr) simplify(exprL)
        else BinExpr("+", simplify(e), simplify(expr))
      case (expr, e@BinExpr("-", exprL, exprR)) =>
        if (exprR == expr) simplify(exprL)
        else BinExpr("+", simplify(expr), simplify(e))

      case (exprL, exprR)      =>
        val sL = simplify(exprL)
        val sR = simplify(exprR)
        if (sL != exprL || sR != exprR) simplify(BinExpr("+", sL, sR)) else BinExpr("+", sL, sR)
    }

    case BinExpr("*", left, right)    => (left, right) match {
      case (expr, IntNum(n))   => if (n == 1) simplify(expr) else if (n == 0) IntNum(0) else {
        val s = simplify(expr)
        if (s != expr) simplify(BinExpr("*", s, IntNum(n))) else BinExpr("*", s, IntNum(n))
      }
      case (IntNum(n), expr)   => if (n == 1) simplify(expr) else if (n == 0) IntNum(0)   else {
        val s = simplify(expr)
        if (s != expr) simplify(BinExpr("*", s, IntNum(n))) else BinExpr("*", s, IntNum(n))
      }
      case (expr, FloatNum(n)) => if (n == 1) simplify(expr) else if (n == 0) FloatNum(0) else {
        val s = simplify(expr)
        if (s != expr) simplify(BinExpr("*", s, FloatNum(n))) else BinExpr("*", s, FloatNum(n))
      }
      case (FloatNum(n), expr) => if (n == 1) simplify(expr) else if (n == 0) FloatNum(0) else {
        val s = simplify(expr)
        if (s != expr) simplify(BinExpr("*", s, FloatNum(n))) else BinExpr("*", s, FloatNum(n))
      }

      // power laws:
      case (BinExpr("**", leftL, rightL), BinExpr("**", leftR, rightR)) if leftL == leftR =>
        simplify(BinExpr("**", leftL, BinExpr("+", rightL, rightR))) // TODO: czy potrzebny wewnetrzny simplify?

      case (expr, BinExpr("/", exprNum, exprDenom)) => simplify(BinExpr("/", BinExpr("*", expr, exprNum), exprDenom))
      case (BinExpr("/", exprNum, exprDenom), expr) => simplify(BinExpr("/", BinExpr("*", expr, exprNum), exprDenom))
      case (exprL, exprR)      =>
        val sL = simplify(exprL)
        val sR = simplify(exprR)
        if (sL != exprL || sR != exprR) simplify(BinExpr("*", sL, sR)) else BinExpr("*", sL, sR)
    }

    case BinExpr("/", left, right) => (left, right) match {
      case (exprL, exprR) if exprL == exprR => IntNum(1)
      // nazwy ponizej moga nie byc najbardziej czytelne, ale to raczej przez specyfike problemu :)
      case (exprNum, BinExpr("/", denomNum, denomDenom)) =>
        val sNum = simplify(exprNum)
        val sDenomNum = simplify(denomNum)
        val sDenomDenom = simplify(denomDenom)
        sNum match {
          case BinExpr("/", sNumNum, sNumDenom) =>
            simplify(BinExpr("/", BinExpr("*", sNumNum, sDenomDenom), BinExpr("*", sNumDenom, sDenomNum)))
          case expr => simplify(BinExpr("/", BinExpr("*", expr, sDenomDenom), sDenomNum))
        }

      // power laws:
      case (BinExpr("**", leftL, rightL), BinExpr("**", leftR, rightR)) if leftL == leftR =>
        simplify(BinExpr("**", leftL, BinExpr("-", rightL, rightR))) // TODO: czy potrzebny wewnetrzny simplify?

      case (expr, IntNum(n))   if n == 1 => simplify(expr)
      case (expr, FloatNum(n)) if n == 1 => simplify(expr)
      case (exprL, exprR) =>
        val sL = simplify(exprL)
        val sR = simplify(exprR)
        if (sL != exprL || sR != exprR) simplify(BinExpr("/", sL, sR)) else BinExpr("/", sL, sR)
    }

    case BinExpr("**", left, right)    => (simplify(left), simplify(right)) match {
      case (expr, IntNum(n))   => if (n == 1) simplify(expr) else if (n == 0) IntNum(1) else {
        val s = simplify(expr)
        if (s != expr) simplify(BinExpr("**", s, IntNum(n))) else BinExpr("**", s, IntNum(n))
      }
      case (IntNum(n), expr)   => if (n == 1) simplify(expr) else if (n == 0) IntNum(1)   else {
        val s = simplify(expr)
        if (s != expr) simplify(BinExpr("**", s, IntNum(n))) else BinExpr("**", s, IntNum(n))
      }
      case (expr, FloatNum(n)) => if (n == 1) simplify(expr) else if (n == 0) FloatNum(1) else {
        val s = simplify(expr)
        if (s != expr) simplify(BinExpr("**", s, FloatNum(n))) else BinExpr("**", s, FloatNum(n))
      }
      case (FloatNum(n), expr) => if (n == 1) simplify(expr) else if (n == 0) FloatNum(1) else {
        val s = simplify(expr)
        if (s != expr) simplify(BinExpr("**", s, FloatNum(n))) else BinExpr("**", s, FloatNum(n))
      }

      // power laws:
      //case (BinExpr("**", IntNum(x), IntNum(y)), expr) => simplify(BinExpr("**", IntNum(x), BinExpr("**", IntNum(y), expr))) // dla testow tylko
      case (BinExpr("**", l, r), expr) => simplify(BinExpr("**", l, BinExpr("*", r, expr))) // to powinno byc, tego powyzej -- nie

      case (exprL, exprR)      =>
        val sL = simplify(exprL)
        val sR = simplify(exprR)
        if (sL != exprL || sR != exprR) simplify(BinExpr("**", sL, sR)) else BinExpr("**", sL, sR)
    }

    case BinExpr("and", left, right) =>
      val sLeft = simplify(left)
      val sRight = simplify(right)
      (sLeft, sRight) match {
        case (_, FalseConst()) => FalseConst()
        case (FalseConst(), _) => FalseConst()
        case (expr, TrueConst()) => expr
        case (TrueConst(), expr) => expr
        case (exprL, exprR) if exprL == exprR => exprL
        case (exprL, exprR) =>
          if (exprL != left || exprR != right) simplify(BinExpr("and", exprL, exprR))
          else BinExpr("and", exprL, exprR)
      }

    case BinExpr("or", left, right) =>
      val sLeft = simplify(left)
      val sRight = simplify(right)
      (sLeft, sRight) match {
        case (_, TrueConst()) => TrueConst()
        case (TrueConst(), _) => TrueConst()
        case (expr, FalseConst()) => expr
        case (FalseConst(), expr) => expr
        case (exprL, exprR) if exprL == exprR => exprL
        case (exprL, exprR) =>
          if (exprL != left || exprR != right) simplify(BinExpr("or", exprL, exprR))
          else BinExpr("or", exprL, exprR)
      }

    // </upraszczanie wyrazen binarnych typu x + 0> --------------------------------------------------------------

    // jesli mamy liste node'ow, to upraszczamy kazdy element z osobna:
    case NodeList(list) => list match {
      case Nil => EmptyInstr()
      case (nl::Nil) => nl match {
        case EmptyInstr() => EmptyInstr()
        case NodeList(l)  => simplify(NodeList(l map simplify)) // zostawiamy tylko jeden layer node listow
        case n            =>
          val sN = simplify(n)
          if (sN != n) simplify(NodeList(List(simplify(n)))) else NodeList(List(sN))
      }
      case _   =>
        val sList = (list map simplify).foldRight(List.empty[Node])(
          (n: Node, list2: List[Node]) => list2 match {
            case Nil   => List(n)
            case x::xs => (n, x) match {
              case (Assignment(lvalN, rvalN), Assignment(lvalX, rvalX)) =>
                if (lvalN == lvalX) x::xs else n::x::xs
              case _ => x::xs
            }
          }
        ).reverse

        val change = (list.length != sList.length) && ((list zip sList) exists (p => p._1 != p._2))
        if (change) simplify(NodeList(sList)) else NodeList(sList)
    }
    // w pozostalych przypadkach nie da sie juz nic uproscic:
    case n => n
  }

}
