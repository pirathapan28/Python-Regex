import unittest
from regex_functions import *


class TestIsRegex(unittest.TestCase):

    def test_is_regex1(self):
        result = is_regex('1')
        self.assertTrue(result)

    def test_is_regex2(self):
        result = is_regex('wot')
        self.assertFalse(result)

    def test_is_regex3(self):
        result = is_regex('()')
        self.assertFalse(result)

    def test_is_regex4(self):
        result = is_regex('(((1.(0|2)*).0)')
        self.assertFalse(result)

    def test_is_regex5(self):
        result = is_regex("(((((1.(0|2)*).(0|(1|e*)))|((1.(0|2)*).(0|(1|e*))"
        "))|(((1.(0|2)*).(0|(1|e*)))|((1.(0|2)*).(0|(1|e*)))))|"
        "((((1.(0|2)*).(0|(1|e*)))|((1.(0|2)*).(0|(1|e*))))"
        "|(((1.(0|2)*).(0|(1|e*)))|((1.(0|2)*).(0|(1|e*))))))")
        self.assertTrue(result)

    def test_is_regex6(self):
        result = is_regex('*(e*.2)')
        self.assertFalse(result)

    def test_is_regex7(self):
        result = is_regex('(*e.2)')
        self.assertFalse(result)

    def test_is_regex8(self):
        result = is_regex('((1.e*).((0.2))')
        self.assertFalse(result)

    def test_is_regex9(self):
        result = is_regex('(1)')
        self.assertFalse(result)

    def test_is_regex9(self):
        result = is_regex('(1.(0.((e*.2)***.(e.0))))')
        self.assertTrue(result)

    def test_is_regex10(self):
        result = is_regex('(1.(0.((e*.2)***.*(e.0))))')
        self.assertFalse(result)

    def test_is_regex11(self):
        result = is_regex('((((1.2).(1|(2|e))**.(e.1)')
        self.assertFalse(result)

    def test_is_regex12(self):
        result = is_regex('((1|2)*.(0*|(e.2*)))*))')
        self.assertFalse(result)

    def test_is_regex13(self):
        result = is_regex('(2*(.)2.1)')
        self.assertFalse(result)


class TestBuildRegexTree(unittest.TestCase):

    def test_tree1(self):
        result = build_regex_tree('1*')
        expected = StarTree(Leaf('1'))
        self.assertEqual(result, expected)

    def test_tree2(self):
        result = build_regex_tree('(2*|e)')
        expected = BarTree(StarTree(Leaf('2')), Leaf('e'))
        self.assertEqual(result, expected)

    def test_tree3(self):
        result = build_regex_tree('(1.(e.2*)*)')
        expected = DotTree(Leaf('1'), StarTree(DotTree(Leaf('e'), StarTree(
            Leaf('2')))))
        self.assertEqual(result, expected)

    def test_tree4(self):
        result = build_regex_tree('(((e|2).0*).(2|0)*)')
        expected = DotTree(DotTree(BarTree(Leaf('e'), Leaf('2')), StarTree(
            Leaf('0'))), StarTree(BarTree(Leaf('2'), Leaf('0'))))
        self.assertEqual(result, expected)

    def test_tree5(self):
        result = build_regex_tree('((0.(1*.2)*)|(e*.1))*')
        expected = StarTree(BarTree(DotTree(Leaf('0'), StarTree(DotTree(
            StarTree(Leaf('1')), Leaf('2')))), DotTree(StarTree(Leaf('e')),
                                                       Leaf('1'))))
        self.assertEqual(result, expected)


class TestRegexMatch(unittest.TestCase):

    def test_match1(self):
        tree = build_regex_tree('1')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match2(self):
        tree = build_regex_tree('e')
        result = regex_match(tree, '')
        self.assertTrue(result)

    def test_match3(self):
        tree = build_regex_tree('(2.1)')
        result = regex_match(tree, '21')
        self.assertTrue(result)

    def test_match4(self):
        tree = build_regex_tree('(1.2)')
        result = regex_match(tree, '21')
        self.assertFalse(result)

    def test_match5(self):
        tree = build_regex_tree('(1.(2.0))')
        result = regex_match(tree, '120')
        self.assertTrue(result)

    def test_match6(self):
        tree = build_regex_tree('((2.1).0)')
        result = regex_match(tree, '21000')
        self.assertFalse(result)

    def test_match7(self):
        tree = build_regex_tree('e')
        result = regex_match(tree, '1')
        self.assertFalse(result)

    def test_match8(self):
        tree = build_regex_tree('(1.e)')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match9(self):
        tree = build_regex_tree('((1.0).(2.1))')
        result = regex_match(tree, '1021')
        self.assertTrue(result)

    def test_match10(self):
        tree = build_regex_tree('((1.0).(e.2))')
        result = regex_match(tree, '102')
        self.assertTrue(result)

    def test_match11(self):
        tree = build_regex_tree('((1.0).(e.2))')
        result = regex_match(tree, '1002')
        self.assertFalse(result)

    def test_match12(self):
        tree = build_regex_tree('((((1.2).0).1).2)')
        result = regex_match(tree, '12012')
        self.assertTrue(result)

    def test_match13(self):
        tree = build_regex_tree('((((1.2).0).1).2)')
        result = regex_match(tree, '120120')
        self.assertFalse(result)

    def test_match14(self):
        tree = build_regex_tree('(1|2)')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match15(self):
        tree = build_regex_tree('(1|2)')
        result = regex_match(tree, '2')
        self.assertTrue(result)

    def test_match16(self):
        tree = build_regex_tree('(1|2)')
        result = regex_match(tree, '12')
        expected = False
        self.assertEqual(result, expected)

    def test_match17(self):
        tree = build_regex_tree('(1|(1.2))')
        result = regex_match(tree, '12')
        self.assertTrue(result)

    def test_match18(self):
        tree = build_regex_tree('(1|(1.2))')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match19(self):
        tree = build_regex_tree('(1|(0.2))')
        result = regex_match(tree, '102')
        expected = False
        self.assertEqual(result, expected)

    def test_match20(self):
        tree = build_regex_tree('(1|(0.2))')
        result = regex_match(tree, '12')
        #expected = False
        self.assertFalse(result)

    def test_match21(self):
        tree = build_regex_tree('(0.2)')
        result = regex_match(tree, '2')
        expected = False
        self.assertEqual(result, expected)

    def test_match22(self):
        tree = build_regex_tree('((1.2)|(0.1))')
        result = regex_match(tree, '1201')
        self.assertFalse(result)

    def test_match23(self):
        tree = build_regex_tree('((1.2)|(0.1))')
        result = regex_match(tree, '12')
        self.assertTrue(result)

    def test_match24(self):
        tree = build_regex_tree('(1|(2.e))')
        result = regex_match(tree, '2')
        self.assertTrue(result)

    def test_match25(self):
        tree = build_regex_tree('(0|(1.(2|e)))')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match26(self):
        tree = build_regex_tree('(0|(1.(2|e)))')
        result = regex_match(tree, '12')
        self.assertTrue(result)

    def test_match27(self):
        tree = build_regex_tree('(0|(1.(2|e)))')
        result = regex_match(tree, '0')
        self.assertTrue(result)

    def test_match28(self):
        tree = build_regex_tree('(0|(1.(2|e)))')
        result = regex_match(tree, '01')
        self.assertFalse(result)

    def test_match28_1(self):
        tree = build_regex_tree('((1.2)|(0|2))')
        result = regex_match(tree, '0')
        self.assertTrue(result)

    def test_match29(self):
        tree = build_regex_tree('(1.2)*')
        result = regex_match(tree, '')
        self.assertTrue(result)

    def test_match30(self):
        tree = build_regex_tree('((e.2)*|1)')
        result = regex_match(tree, '')
        self.assertTrue(result)

    def test_match31(self):
        tree = build_regex_tree('((e.2)*|1)')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match32(self):
        tree = build_regex_tree('1*')
        result = regex_match(tree, '11')

    def test_match33(self):
        tree = build_regex_tree('1*')
        result = regex_match(tree, '')
        self.assertTrue(result)

    def test_match33_1(self):
        tree = build_regex_tree('1*')
        result = regex_match(tree, '12')
        self.assertFalse(result)

    def test_match33_2(self):
        tree = build_regex_tree('2*')
        result = regex_match(tree, '222000')
        self.assertFalse(result)

    def test_match34(self):
        tree = build_regex_tree('2*')
        result = regex_match(tree, '212')
        self.assertFalse(result)

    def test_match35(self):
        tree = build_regex_tree('(1*.2)')
        result = regex_match(tree, '2')
        self.assertTrue(result)

    def test_match36(self):
        tree = build_regex_tree('(1*.2)')
        result = regex_match(tree, '12')
        self.assertTrue(result)

    def test_match37(self):
        tree = build_regex_tree('(1*.2)')
        result = regex_match(tree, '1112')
        self.assertTrue(result)

    def test_match38(self):
        tree = build_regex_tree('(1*.2)')
        result = regex_match(tree, '122')
        self.assertFalse(result)

    def test_match39(self):
        tree = build_regex_tree('(1.2*)')
        result = regex_match(tree, '1222')
        self.assertTrue(result)

    def test_match40(self):
        tree = build_regex_tree('(1.2*)')
        result = regex_match(tree, '112')
        self.assertFalse(result)

    def test_match41(self):
        tree = build_regex_tree('(1.2*)')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match41(self):
        tree = build_regex_tree('e*')
        result = regex_match(tree, '')

    def test_match42(self):
        tree = build_regex_tree('e*')
        result = regex_match(tree, 'eee')
        self.assertFalse(result)

    def test_match43(self):
        tree = build_regex_tree('(e.1*)')
        result = regex_match(tree, '111')
        self.assertTrue(result)

    def test_match44(self):
        tree = build_regex_tree('(e**.1**)')
        result = regex_match(tree, '')
        self.assertTrue(result)

    def test_match45(self):
        tree = build_regex_tree('(e*.1***)')
        result = regex_match(tree, '1111111111')
        self.assertTrue(result)

    def test_match46(self):
        tree = build_regex_tree('(1*.2*)')
        result = regex_match(tree, '')
        self.assertTrue(result)

    def test_match47(self):
        tree = build_regex_tree('(1*.2*)')
        result = regex_match(tree, '12')
        self.assertTrue(result)

    def test_match48(self):
        tree = build_regex_tree('(1*.2*)')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match48(self):
        tree = build_regex_tree('(1*.2*)')
        result = regex_match(tree, '2')
        self.assertTrue(result)

    def test_match48(self):
        tree = build_regex_tree('(1*.2*)')
        result = regex_match(tree, '111')
        self.assertTrue(result)

    def test_match48(self):
        tree = build_regex_tree('(1*.2*)')
        result = regex_match(tree, '2222')
        self.assertTrue(result)

    def test_match48(self):
        tree = build_regex_tree('(1*.2*)')
        result = regex_match(tree, '1111122222222')
        self.assertTrue(result)

    def test_match48(self):
        tree = build_regex_tree('(1*|2*)')
        result = regex_match(tree, '')
        self.assertTrue(result)

    def test_match49(self):
        tree = build_regex_tree('(1*|2*)')
        result = regex_match(tree, '111')
        self.assertTrue(result)

    def test_match49(self):
        tree = build_regex_tree('(1*|2*)')
        result = regex_match(tree, '2222')
        self.assertTrue(result)

    def test_match50(self):
        tree = build_regex_tree('(1*|2*)')
        result = regex_match(tree, '1122')
        self.assertFalse(result)

    def test_match51(self):
        tree = build_regex_tree('(1*.(2|0))')
        result = regex_match(tree, '11110')
        self.assertTrue(result)

    def test_match52(self):
        tree = build_regex_tree('(1*.(2|0))')
        result = regex_match(tree, '2')
        self.assertTrue(result)

    def test_match53(self):
        tree = build_regex_tree('(1*.(2|0))')
        result = regex_match(tree, '20')
        self.assertFalse(result)

    def test_match54(self):
        tree = build_regex_tree('(1*.(2|0))')
        result = regex_match(tree, '1111112')
        self.assertTrue(result)

    def test_match55(self):
        tree = build_regex_tree('(1*.(2|0))')
        result = regex_match(tree, '11122')
        self.assertFalse(result)

    def test_match56(self):
        tree = build_regex_tree('((1.2**).(0**|2))')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match57(self):
        tree = build_regex_tree('((1.2**).(0**|2))')
        result = regex_match(tree, '12222000')
        self.assertTrue(result)

    def test_match58(self):
        tree = build_regex_tree('((1.2**).(0**|2))')
        result = regex_match(tree, '12')
        self.assertTrue(result)

    def test_match59(self):
        tree = build_regex_tree('((1.2**).(0**|2))')
        result = regex_match(tree, '12222200002')
        self.assertFalse(result)

    def test_match60(self):
        tree = build_regex_tree('((1.2**).(0**|2))')
        result = regex_match(tree, '102')
        self.assertFalse(result)

    def test_match61(self):
        tree = build_regex_tree('(1.2)*')
        result = regex_match(tree, '12')
        self.assertTrue(result)

    def test_match62(self):
        tree = build_regex_tree('(1.2)*')
        result = regex_match(tree, '121212')
        self.assertTrue(result)

    def test_match63(self):
        tree = build_regex_tree('(1.2)*')
        result = regex_match(tree, '212121')
        self.assertFalse(result)

    def test_match64(self):
        tree = build_regex_tree('(1|2)*')
        result = regex_match(tree, '12')
        self.assertTrue(result)

    def test_match65(self):
        tree = build_regex_tree('(1|2)*')
        result = regex_match(tree, '1221212212')
        self.assertTrue(result)

    def test_match66(self):
        tree = build_regex_tree('(1*.1)')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match67(self):
        tree = build_regex_tree('(1*.2)')
        result = regex_match(tree, '11')
        self.assertFalse(result)

    def test_match68(self):
        tree = build_regex_tree('(1*.2)')
        result = regex_match(tree, '11111112')
        self.assertTrue(result)

    def test_match69(self):
        tree = build_regex_tree('(1*.2)*')
        result = regex_match(tree, '1112111112112')
        self.assertTrue(result)

    def test_match70(self):
        tree = build_regex_tree('(1*.2)*')
        result = regex_match(tree, '11211112222112')
        self.assertTrue(result)

    def test_match71(self):
        tree = build_regex_tree('((1.2)*.1)')
        result = regex_match(tree, '1212121')
        self.assertTrue(result)

    def test_match72(self):
        tree = build_regex_tree('((1.2)*.1)*')
        result = regex_match(tree, '12121211212121')
        self.assertTrue(result)

    def test_match73(self):
        tree = build_regex_tree('((1.2)*.1)*')
        result = regex_match(tree, '1211211')
        self.assertTrue(result)

    def test_match74(self):
        tree = build_regex_tree('((1.2)*.1)*')
        result = regex_match(tree, '1212')
        self.assertFalse(result)

    def test_match75(self):
        tree = build_regex_tree('(0.(1.2)*)*')
        result = regex_match(tree, '0')
        self.assertTrue(result)

    def test_match76(self):
        tree = build_regex_tree('(0.(1.2)*)*')
        result = regex_match(tree, '012')
        self.assertTrue(result)

    def test_match77(self):
        tree = build_regex_tree('(0.(1.2)*)*')
        result = regex_match(tree, '0000')
        self.assertTrue(result)

    def test_match78(self):
        tree = build_regex_tree('(0.(1.2)*)*')
        result = regex_match(tree, '01201200000121212')
        self.assertTrue(result)

    def test_match79(self):
        tree = build_regex_tree('(0.(1.2)*)*')
        result = regex_match(tree, '0120102')
        self.assertFalse(result)

    def test_match80(self):
        tree = build_regex_tree('((1|2)*|(0.1))*')
        result = regex_match(tree, '1')
        self.assertTrue(result)

    def test_match81(self):
        tree = build_regex_tree('((1|2)*|(0.1))*')
        result = regex_match(tree, '010101')
        self.assertTrue(result)

    def test_match82(self):
        tree = build_regex_tree('((1|2)*|(0.1))*')
        result = regex_match(tree, '12')
        self.assertTrue(result)

    def test_match83(self):
        tree = build_regex_tree('((1|2)*|(0.1))*')
        result = regex_match(tree, '202')
        self.assertFalse(result)

    def test_match84(self):
        tree = build_regex_tree('((1|2)*|(0.1))*')
        result = regex_match(tree, '010101')
        self.assertTrue(result)

    def test_match85(self):
        tree = build_regex_tree('((1|2)*|(0.1))*')
        result = regex_match(tree, '121212010101121212010101')
        self.assertTrue(result)

    def test_match86(self):
        tree = build_regex_tree('((1|2)*|(0.1))*')
        result = regex_match(tree, '12121201010112121200101')
        self.assertFalse(result)

    def test_match87(self):
        tree = build_regex_tree('((1.2)*.((1.2).0))')
        result = regex_match(tree, '120')
        self.assertTrue(result)

    def test_match88(self):
        tree = build_regex_tree('((1.2)*.((1.2).0))')
        result = regex_match(tree, '1212120')
        self.assertTrue(result)

    def test_match89(self):
        tree = build_regex_tree('((1.2)*.((1.2).0))')
        result = regex_match(tree, '')
        self.assertFalse(result)

    def test_match90(self):
        tree = build_regex_tree('(((1.2).0)*.((0.1).2))')
        result = regex_match(tree, '012')
        self.assertTrue(result)

    def test_match90(self):
        tree = build_regex_tree('(((1.2).0)*.((0.1).2))')
        result = regex_match(tree, '120012')
        self.assertTrue(result)

    def test_match90(self):
        tree = build_regex_tree('(((1.2).0)*.((0.1).2))')
        result = regex_match(tree, '12312')
        self.assertFalse(result)

    def test_match91(self):
        tree = build_regex_tree('((e.1)*|0)')
        result = regex_match(tree, '1111')
        self.assertTrue(result)

    def test_match92(self):
        tree = build_regex_tree('((e.1)*|0)')
        result = regex_match(tree, '00')
        self.assertFalse(result)

    def test_match93(self):
        tree = build_regex_tree('((0.(1*.2)*)|(e*.1))*')
        result = regex_match(tree, '0')
        self.assertTrue(result)

    def test_match94(self):
        tree = build_regex_tree('((0.(1*.2)*)|(e*.1))*')
        result = regex_match(tree, '1111')
        self.assertTrue(result)

    def test_match95(self):
        tree = build_regex_tree('((0.(1*.2)*)|(e*.1))*')
        result = regex_match(tree, '01112121111112')
        self.assertTrue(result)

    def test_match96(self):
        tree = build_regex_tree('((0.(1*.2)*)|(e*.1))*')
        result = regex_match(tree, '0111212111111201112121111112')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main(exit=False)
