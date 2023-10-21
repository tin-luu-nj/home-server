from src.pyFileManagement import walk_tree

from _ut_template import clsUnitTestTemplate


class Test_Normal(clsUnitTestTemplate):
    @clsUnitTestTemplate._template_decorate
    def test_FMGR_UT_001(self):
        self.check(walk_tree())

    @clsUnitTestTemplate._template_decorate
    def test_FMGR_UT_002(self):
        self.check(walk_tree())

    @clsUnitTestTemplate._template_decorate
    def test_FMGR_UT_003(self):
        self.check(walk_tree())

    @clsUnitTestTemplate._template_decorate
    def test_FMGR_UT_004(self):
        self.check(walk_tree())


################################################################################
#                                END OF FILE                                   #
################################################################################
