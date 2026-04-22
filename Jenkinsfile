// Jenkinsfile - API自动化测试流水线配置
// 校园二手交易平台接口自动化测试

pipeline {
    agent any
    
    environment {
        // 测试环境配置
        TEST_ENV = 'test'
        PYTHON_VERSION = '3.9'
        PROJECT_DIR = 'apiautotest'
        
        // 报告路径
        ALLURE_RESULTS = 'reports/allure-results'
        ALLURE_REPORT = 'reports/allure-report'
    }
    
    options {
        // 构建超时时间（分钟）
        timeout(time: 30, unit: 'MINUTES')
        
        // 保留最近10次构建记录
        buildDiscarder(logRotator(numToKeepStr: '10'))
        
        // 禁止并发构建
        disableConcurrentBuilds()
    }
    
    stages {
        stage(' Checkout Code') {
            steps {
                script {
                    echo '=== 拉取最新代码 ==='
                    checkout scm
                }
            }
        }
        
        stage('🔧 Setup Environment') {
            steps {
                script {
                    echo '=== 配置Python环境 ==='
                    dir(PROJECT_DIR) {
                        sh '''
                            # 创建虚拟环境
                            python3 -m venv venv
                            
                            # 激活虚拟环境并安装依赖
                            source venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            
                            # 验证安装
                            python --version
                            pytest --version
                        '''
                    }
                }
            }
        }
        
        stage('🧪 Run API Tests') {
            steps {
                script {
                    echo '=== 执行API自动化测试 ==='
                    dir(PROJECT_DIR) {
                        sh '''
                            source venv/bin/activate
                            
                            # 运行测试并生成Allure数据
                            # 只运行 user 模块的测试
                            python run.py --env ${TEST_ENV} --module user --allure
                        '''
                    }
                }
            }
            post {
                success {
                    echo '测试执行成功！'
                }
                failure {
                    echo '测试执行失败！'
                    // 即使失败也继续生成报告
                }
            }
        }
        
        stage('📊 Generate Allure Report') {
            steps {
                script {
                    echo '=== 生成Allure测试报告 ==='
                    dir(PROJECT_DIR) {
                        // 使用Allure插件生成报告
                        allure includeProperties: false, 
                              jdk: '', 
                              results: [[path: ALLURE_RESULTS]]
                    }
                }
            }
        }
        
        stage('📧 Send Notification') {
            steps {
                script {
                    echo '=== 发送测试报告通知 ==='
                    
                    // 获取构建结果
                    def result = currentBuild.result ?: 'SUCCESS'
                    def recipients = '13553204558@163.com'
                    
                    if (result == 'SUCCESS') {
                        echo '✅ 测试通过，发送成功通知'
                        mail to: recipients,
                             subject: "✅ [PASS] API自动化测试 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                             mimeType: 'text/html',
                             body: """
                                 <html>
                                 <body style="font-family: Arial, sans-serif;">
                                     <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                                         <h2 style="color: #28a745;">✅ 测试执行成功</h2>
                                         <hr style="border: 1px solid #eee;">
                                         <table style="width: 100%; border-collapse: collapse;">
                                             <tr><td style="padding: 8px; font-weight: bold;">项目:</td><td style="padding: 8px;">${env.JOB_NAME}</td></tr>
                                             <tr style="background-color: #f9f9f9;"><td style="padding: 8px; font-weight: bold;">构建号:</td><td style="padding: 8px;">#${env.BUILD_NUMBER}</td></tr>
                                             <tr><td style="padding: 8px; font-weight: bold;">环境:</td><td style="padding: 8px;">${TEST_ENV}</td></tr>
                                             <tr style="background-color: #f9f9f9;"><td style="padding: 8px; font-weight: bold;">构建时间:</td><td style="padding: 8px;">${new Date()}</td></tr>
                                         </table>
                                         <hr style="border: 1px solid #eee;">
                                         <p style="margin: 20px 0;">
                                             <a href="${env.BUILD_URL}allure/" 
                                                style="display: inline-block; padding: 12px 24px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px;">
                                                 📊 查看 Allure 测试报告
                                             </a>
                                         </p>
                                         <p style="color: #28a745; font-size: 16px;">
                                             ✅ 所有测试用例通过！
                                         </p>
                                         <hr style="border: 1px solid #eee;">
                                         <p style="color: #6c757d; font-size: 12px;">
                                             此邮件由 Jenkins 自动发送，请勿回复。
                                         </p>
                                     </div>
                                 </body>
                                 </html>
                             """
                    } else {
                        echo '❌ 测试失败，发送失败通知'
                        mail to: recipients,
                             subject: "❌ [FAIL] API自动化测试 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                             mimeType: 'text/html',
                             body: """
                                 <html>
                                 <body style="font-family: Arial, sans-serif;">
                                     <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                                         <h2 style="color: #dc3545;">❌ 测试执行失败</h2>
                                         <hr style="border: 1px solid #eee;">
                                         <table style="width: 100%; border-collapse: collapse;">
                                             <tr><td style="padding: 8px; font-weight: bold;">项目:</td><td style="padding: 8px;">${env.JOB_NAME}</td></tr>
                                             <tr style="background-color: #f9f9f9;"><td style="padding: 8px; font-weight: bold;">构建号:</td><td style="padding: 8px;">#${env.BUILD_NUMBER}</td></tr>
                                             <tr><td style="padding: 8px; font-weight: bold;">环境:</td><td style="padding: 8px;">${TEST_ENV}</td></tr>
                                             <tr style="background-color: #f9f9f9;"><td style="padding: 8px; font-weight: bold;">构建时间:</td><td style="padding: 8px;">${new Date()}</td></tr>
                                         </table>
                                         <hr style="border: 1px solid #eee;">
                                         <p style="margin: 20px 0;">
                                             <a href="${env.BUILD_URL}console" 
                                                style="display: inline-block; padding: 12px 24px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; margin-right: 10px;">
                                                 🔍 查看构建日志
                                             </a>
                                             <a href="${env.BUILD_URL}allure/" 
                                                style="display: inline-block; padding: 12px 24px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px;">
                                                 📊 查看测试报告
                                             </a>
                                         </p>
                                         <p style="color: #dc3545; font-size: 16px;">
                                             ❌ 存在失败的测试用例，请及时处理！
                                         </p>
                                         <hr style="border: 1px solid #eee;">
                                         <p style="color: #6c757d; font-size: 12px;">
                                             此邮件由 Jenkins 自动发送，请勿回复。
                                         </p>
                                     </div>
                                 </body>
                                 </html>
                             """
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo '=== 清理工作空间 ==='
                dir(PROJECT_DIR) {
                    // 清理虚拟环境（可选，节省空间可保留）
                    // sh 'rm -rf venv'
                    
                    // 清理临时文件
                    sh '''
                        find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
                        find . -type f -name "*.pyc" -delete 2>/dev/null || true
                    '''
                }
            }
        }
        
        success {
            script {
                echo '🎉 流水线执行成功！'
                echo "📊 查看报告: ${env.BUILD_URL}allure/"
            }
        }
        
        failure {
            script {
                echo '⚠️ 流水线执行失败，请检查日志'
                echo "🔍 查看详情: ${env.BUILD_URL}console"
            }
        }
    }
}

/*
 * ============================================================================
 * 定时触发配置（已注释 - 演示用）
 * ============================================================================
 * 
 * 如果需要启用定时触发，取消下面的注释：
 * 
 * 语法说明：
 * ┌───────────── 分钟 (0 - 59)
 * │ ┌───────────── 小时 (0 - 23)
 * │ │ ┌───────────── 日 (1 - 31)
 * │ │ │ ┌───────────── 月 (1 - 12)
 * │ │ │ │ ┌───────────── 星期 (0 - 7) 星期日=0或7
 * │ │ │ │ │
 * * * * * *
 * 
 * 常用示例：
 * H/30 * * * *     : 每30分钟执行一次
 * H 2 * * *        : 每天凌晨2点执行
 * H 9-18 * * 1-5   : 工作日9-18点每小时执行
 * 0 0 * * 0        : 每周日凌晨执行
 * H H(2-4) * * *   : 每天凌晨2-4点随机时间执行
 * 
 * 取消注释下面的 triggers 块即可启用：
 */

triggers {
    // 每天16:15执行
    cron('15 16 * * *')
}

/*
 * ============================================================================
 * 其他可选配置（已注释 - 按需启用）
 * ============================================================================
 */

/*
// 参数化构建配置
parameters {
    choice(
        name: 'TEST_ENV',
        choices: ['dev', 'test', 'prod'],
        description: '选择测试环境'
    )
    
    choice(
        name: 'TEST_MODULE',
        choices: ['all', 'user', 'product', 'admin', 'credit'],
        description: '选择测试模块'
    )
    
    booleanParam(
        name: 'RUN_SMOKE_ONLY',
        defaultValue: false,
        description: '是否只运行冒烟测试'
    )
}

// 根据参数动态调整测试命令
stage('Run API Tests') {
    steps {
        script {
            def moduleArg = params.TEST_MODULE == 'all' ? '' : "--module ${params.TEST_MODULE}"
            def tagArg = params.RUN_SMOKE_ONLY ? '--tag smoke' : ''
            
            sh """
                source venv/bin/activate
                python run.py --env ${params.TEST_ENV} ${moduleArg} ${tagArg} --allure
            """
        }
    }
}
