import openpyxl
import re
from decimal import Decimal, ROUND_HALF_UP

class calculater():
    def __init__(self):
        self.atomic_dict = dict()
        wb = openpyxl.load_workbook("atomic_weights.xlsx")
        ws = wb.worksheets[0]
        for row in ws.iter_rows(min_row = 2, max_col=4, values_only=True):
            # print(row)
            if row[2] == None:  # 終了条件
                break
            if row[0] == None:  # isotopicな同位体だけ追加
                continue

            # 正規表現で上手いこと整数部、小数部、不確かな小数部に分ける
            _list = re.split("[(.]",row[3][:-1])

            # 辞書に追加
            self.atomic_dict[row[1]] = _list[0]+"."+_list[1]+_list[2]

    # now_indから原子量を算出
    # dictに存在しない場合のエラー処理もする
    def get_atomic_weight(self, now_ind):
        # ラスト1文字の例外処理
        if now_ind+1 == self.len_formula:
            atom = self.formula[now_ind]     
            try:
                return atom, self.atomic_dict[atom], 1
            except KeyError:
                return atom, None, None
        # それ以外
        else:
            atom = self.formula[now_ind:now_ind+2]
            try:
                return atom, self.atomic_dict[atom], 2
            except KeyError:
                atom = self.formula[now_ind]
                try:
                    return atom, self.atomic_dict[atom], 1
                except KeyError:
                    return atom, None, None


    def calculate(self, formula):
        self.formula = formula
        self.len_formula = len(formula)
        molecular_weight = 0
        self.len_formula = len(self.formula)
        now_ind = 0
        while now_ind < self.len_formula:
            atom, atomic_weight, len_atom = self.get_atomic_weight(now_ind)
            # dictに存在しない場合、Falseとともに原因の文字を返す
            if atomic_weight == None:
                return False, atom
            
            num_ind = now_ind + len_atom
            # ラスト1文字の例外処理
            if num_ind == self.len_formula:
                molecular_weight += Decimal(atomic_weight)
            else:
                coef = ""
                while num_ind < self.len_formula:
                    try:
                        num = int(formula[num_ind])
                        coef += str(num)
                        num_ind += 1
                    except:
                        break
                if not coef:
                    molecular_weight += Decimal(atomic_weight)
                else:
                    molecular_weight += Decimal(atomic_weight) * int(coef)
            
            now_ind = num_ind
        
        # 数値がでかすぎるとエラーを吐くのでここでも例外処理
        try:
            return True, str(molecular_weight.quantize(Decimal("1E-4"), rounding=ROUND_HALF_UP))
        except ArithmeticError as e:
            return True, "オーバーフロー"


# デバッグ用
if __name__ == "__main__":
    cal = calculater()
    print(cal.calculate("C3H8O"))
