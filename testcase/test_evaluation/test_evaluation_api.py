# testcase/test_evaluation/test_evaluation_api.py
"""
商品评价模块测试
对应YAML: data/evaluation/*.yaml
"""

import pytest
import allure
from testcase.base_test import BaseTest
from core.data_driver import DataDriver


@allure.epic("二手交易平台")
@allure.feature("商品评价模块")
class TestEvaluationAPI(BaseTest):
    """商品评价测试类"""

    driver = DataDriver()

    @allure.story("提交评价")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试提交商品评价接口的各种场景")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("evaluation", "submit.yaml")
    def test_submit_evaluation(self, case_data, login_student):
        """
        测试提交评价
        测试场景：
        - TC-EVAL-001: 好评提交
        - TC-EVAL-002: 差评有证据
        - TC-EVAL-003: 差评无证据
        - TC-EVAL-004~008: 各种异常场景
        """
        response = self.execute(case_data)
        
        # 评价成功后的额外验证
        if response.status_code == 200:
            data = response.json()
            deduction_points = data.get('deduction_points', 0)
        
            # 根据评价类型验证扣分
            case_id = case_data.get('id')
            if case_id == 'TC-EVAL-001':  # 好评
                assert deduction_points == 0, "好评不应扣分"
            elif case_id == 'TC-EVAL-002':  # 差评有证据
                assert deduction_points > 0, "差评应扣分"
        
            # 记录已评价的商品 ID（从 path_params 中获取）
            path_params = case_data.get('path_params', {})
            product_id = path_params.get('first_bought_product_id')
            if product_id:
                # 获取当前已评价商品列表
                from config.dynamic_vars import dynamic_vars
                evaluated_ids = dynamic_vars.get_var('evaluated_product_ids', [])
                        
                # 如果这个 ID 还不在列表中，添加它
                if str(product_id) not in [str(x) for x in evaluated_ids]:
                    evaluated_ids.append(product_id)
                    dynamic_vars.set_var('evaluated_product_ids', evaluated_ids)
                    self.logger.info(f"商品 {product_id} 已评价，已记录到 evaluated_product_ids")
        
            self.logger.info(f"评价提交成功，扣分：{deduction_points}")

