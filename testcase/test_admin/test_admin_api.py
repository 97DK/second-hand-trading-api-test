# testcase/test_admin/test_admin_api.py
"""
管理员模块测试
对应YAML: data/admin/*.yaml
"""

import pytest
import allure
from testcase.base_test import BaseTest
from core.data_driver import DataDriver


@allure.epic("二手交易平台")
@allure.feature("管理员模块")
class TestAdminAPI(BaseTest):
    """管理员接口测试类"""

    driver = DataDriver()

    # ==================== 用户管理 ====================

    @allure.story("用户管理 - 获取用户列表")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试管理员获取用户列表的各种场景")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("admin", "user_manage.yaml")
    def test_user_manage(self, case_data, login_admin):
        """
        测试获取用户管理数据
        测试场景：
        - TC-ADMIN-001: 获取所有用户
        - TC-ADMIN-002: 筛选待审核
        - TC-ADMIN-003: 筛选已审核
        - TC-ADMIN-004: 非管理员访问
        """
        # 对于非管理员访问的测试
        if case_data.get('id') == 'TC-ADMIN-004':
            self.request.clear_auth()
            self.request.login('student', 'sssas', 'TFBOYS2023')

        response = self.execute(case_data)

        if response.status_code == 200:
            users = response.json()
            assert isinstance(users, list)

            # 根据筛选类型验证
            query_params = case_data.get('query_params', {})
            user_type = query_params.get('type')

            if user_type == 'pending':
                # 验证所有用户都是待审核状态
                for user in users:
                    assert user.get('is_verified') is False
                self.logger.info(f"获取待审核用户列表，共 {len(users)} 个")
            elif user_type == 'verified':
                for user in users:
                    assert user.get('is_verified') is True
                self.logger.info(f"获取已审核用户列表，共 {len(users)} 个")
            else:
                self.logger.info(f"获取所有用户列表，共 {len(users)} 个")

    # ==================== 用户审核 ====================

    @allure.story("用户审核")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("测试管理员审核用户的各种场景")
    @pytest.mark.smoke
    @pytest.mark.p0
    @driver.parametrize("admin", "user_audit.yaml")
    def test_user_audit(self, case_data, login_admin):
        """
        测试用户审核操作
        测试场景：
        - TC-ADMIN-005: 通过审核
        - TC-ADMIN-006: 拒绝审核
        - TC-ADMIN-007: 用户不存在
        - TC-ADMIN-008: 无效操作
        """
        response = self.execute(case_data)

        # 审核成功后的额外验证
        if response.status_code == 200:
            case_id = case_data.get('id')
            path_params = case_data.get('path_params', {})
            user_id = path_params.get('user_id')
            action = path_params.get('action')

            if action == 'approve':
                self.logger.info(f"用户 {user_id} 已通过审核")
            elif action == 'reject':
                self.logger.info(f"用户 {user_id} 已被拒绝")

    # ==================== 商品管理 ====================

    @allure.story("商品管理 - 获取商品列表")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试管理员获取商品管理数据")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("admin", "product_list.yaml")
    def test_product_list(self, case_data, login_admin):
        """测试获取商品管理列表"""
        response = self.execute(case_data)

        if response.status_code == 200:
            products = response.json()
            assert isinstance(products, list)
            self.logger.info(f"获取商品管理列表，共 {len(products)} 个")

    @allure.story("商品管理 - 审核操作")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("测试管理员审核商品的各种场景")
    @pytest.mark.smoke
    @pytest.mark.p0
    @driver.parametrize("admin", "product_manage.yaml")
    def test_product_audit(self, case_data, login_admin):
        """
        测试商品审核操作
        测试场景：
        - TC-ADMIN-010: 通过商品
        - TC-ADMIN-011: 拒绝商品
        - TC-ADMIN-012: 下架商品
        - TC-ADMIN-013~015: 参数异常
        """
        response = self.execute(case_data)

        if response.status_code == 200:
            data = case_data.get('data', {})
            action = data.get('action')
            product_id = data.get('product_id')

            action_map = {
                'approve': '上架',
                'reject': '拒绝',
                'remove': '下架'
            }
            self.logger.info(f"商品 {product_id} 已{action_map.get(action, action)}")

    # ==================== 心愿管理 ====================

    @allure.story("心愿管理 - 获取心愿列表")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试管理员获取心愿管理数据")
    @pytest.mark.regression
    @pytest.mark.p2
    @driver.parametrize("admin", "wish_list.yaml")
    def test_wish_list(self, case_data, login_admin):
        """测试获取心愿管理列表"""
        response = self.execute(case_data)

        if response.status_code == 200:
            wishes = response.json()
            assert isinstance(wishes, list)
            self.logger.info(f"获取心愿管理列表，共 {len(wishes)} 个")

    @allure.story("心愿管理 - 审核操作")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试管理员审核心愿的各种场景")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("admin", "wish_manage.yaml")
    def test_wish_audit(self, case_data, login_admin):
        """
        测试心愿审核操作
        测试场景：
        - TC-ADMIN-017: 通过心愿
        - TC-ADMIN-018: 拒绝心愿
        """
        self.execute(case_data)

    # ==================== 申诉管理 ====================

    @allure.story("申诉管理 - 获取申诉列表")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试管理员获取申诉管理数据")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("admin", "appeal_list.yaml")
    def test_appeal_list(self, case_data, login_admin):
        """测试获取申诉管理列表"""
        response = self.execute(case_data)

        # 检查response是否为None
        if response is None:
            self.logger.error("请求返回None，测试失败")
            assert False, "请求返回None"
            
        if response.status_code == 200:
            appeals = response.json()
            assert isinstance(appeals, list)
            self.logger.info(f"获取申诉管理列表，共 {len(appeals)} 个")

    @allure.story("申诉管理 - 审核操作")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("测试管理员审核申诉的各种场景")
    @pytest.mark.smoke
    @pytest.mark.p0
    @driver.parametrize("admin", "appeal_manage.yaml")
    def test_appeal_audit(self, case_data, login_admin):
        """
        测试申诉审核操作
        测试场景：
        - TC-ADMIN-020: 通过申诉
        - TC-ADMIN-021: 驳回申诉
        - TC-ADMIN-022~024: 参数异常
        """
        response = self.execute(case_data)

        if response.status_code == 200:
            data = case_data.get('data', {})
            evaluation_id = data.get('evaluation_id')
            action = data.get('action')

            action_map = {
                'approve': '通过',
                'reject': '驳回'
            }
            self.logger.info(f"申诉 {evaluation_id} 已{action_map.get(action, action)}")