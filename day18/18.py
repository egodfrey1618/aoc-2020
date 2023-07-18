class Expression(object):
    def __init__(self, s):
        self._line = []
        self._s = s
        i = 0
        while i < len(s):
            c = s[i]
            if c == " ": 
                pass
            elif c == "(":
                # Find the matching bracket
                count = 1
                for j in range(i+1, len(s)):
                    if s[j] == "(": count += 1
                    if s[j] == ")": count -= 1
                    if count == 0: break
                else:
                    assert False, "couldn't find matching bracket"
                self._line.append(Expression(s[i+1:j]))
                i = j
            elif c in "0123456789":
                self._line.append(int(c))
            elif c == ")":
                assert False, "found closing bracket without opening"
            elif c in "+*":
                self._line.append(c)
            else:
                assert False, "unknown char"
            i += 1

    def eval_rec(self, eval_base):
        def eval_if_exp(e):
            if type(e) == Expression:
                return e.eval_rec(eval_base)
            else:
                return e

        assert len(self._line) >= 1
        assert len(self._line) & 1 == 1

        # Evaluate any subexpressions.
        l = [eval_if_exp(e) for e in self._line]

        # Evaluate now we've resolved everything.
        return eval_base(l)

    def eval_basic(self):
        # No operator precedence with this!
        def eval_base(base_exp):
            result = base_exp[0]

            for i in range(1, len(base_exp), 2):
                operation = base_exp[i]
                next_value = base_exp[i+1]

                if operation == "+":
                    result += next_value
                elif operation == "*":
                    result *= next_value
                else:
                    assert False
            return result
        return self.eval_rec(eval_base)

    def eval_advanced(self):
        # Operator precedence - addition comes before multiplication.
        def eval_base(base_exp):
            # 2 passes - first pass, collect up any additions. 
            for i in range(1, len(base_exp), 2):
                operation = base_exp[i]
                next_value = base_exp[i+1]

                if operation == "+":
                    base_exp[i+1] += base_exp[i-1]
                    base_exp[i-1] = 1
                    base_exp[i] = "*"

            # Second pass - I've turned all the instructions into multiplications now.
            result = 1
            for i in range(0, len(base_exp), 2):
                result *= base_exp[i]
            return result
        return self.eval_rec(eval_base)


exps = []
for line in open("input"):
    exps.append(Expression(line.strip()))
print(sum(e.eval_basic() for e in exps))
print(sum(e.eval_advanced() for e in exps))

def test(s):
    print(Expression(s).eval_advanced())
