import React from 'react';
import { Button, Card, Checkbox, Form, Input, message, Modal } from 'antd';
import axios from 'axios';
import Agreement from '../components/Agreement';
import configs from './config';
import './Login.less';
import { getUserFromQuery } from './tools';

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      qq: '',
      stuId: '',
      passwd: '',
      token: '',
      agreeDeal: true,
      loginStatus: null,
      AgreeContentModalVisible: false,
    };
  }
  componentDidMount() {
    const user = getUserFromQuery();
    this.setState({
      qq: user.qq,
      token: user.token,
    });
  }

  handleIdInput = (e) => {
    this.setState({
      stuId: e.target.value,
    });
  };
  handlePwdInput = (e) => {
    this.setState({
      passwd: e.target.value,
    });
  };
  handleLogin = (e) => {
    if (this.state.stuId && this.state.passwd && this.state.token) {
      this.setState({
        loginStatus: 'loading',
      });
      let login_data = {
        username: this.state.stuId,
        password: this.state.passwd,
        qq: this.state.qq,
        token: this.state.token,
      };
      axios
        .post(configs.apiUrl + '/api/user/bind', login_data)
        .then((res) => {
          if (res.status == '200' && res.data.code == '200') {
            message.success(`登录成功！请返回聊天页面。`);
            this.setState({
              loginStatus: 'success',
            });
          } else if (res.status == '200' && res.data.code == '-1') {
            if (res.data.data == 'qq绑定失败!失败原因是AuthFail') {
              message.error(`绑定失败！用户名密码错误！`);
            } else if (res.data.data == '该qq已经绑定了!') {
              message.error(`该 QQ 已绑定！`);
            } else {
              message.error(`绑定失败，教务处暂时无法访问！`);
            }
            this.setState({
              loginStatus: 'fail',
            });
          }
        })
        .catch((err) => {
          if (err.response && err.response.status == 403) {
            message.error('参数请求错误!');
          } else {
            message.error(`登录失败:${err.response.status}，请检查网络连接!`);
          }
          this.setState({
            loginStatus: 'fail',
          });
        });
    } else {
      message.error('请输入账号密码！');
    }
  };

  onClose = () => {
    this.setState({
      agreeDeal: false,
      AgreeContentModalVisible: false,
    });
  };

  handleAgreeCheckboxClick = () => {
    this.setState({
      agreeDeal: !this.state.agreeDeal,
    });
  };

  handleAgreeButtonClick = () => {
    this.setState({
      agreeDeal: true,
      AgreeContentModalVisible: false,
    });
  };
  click = () => {
    this.setState({
      AgreeContentModalVisible: true,
    });
  };
  render() {
    let a = true;
    let loginButtonIcon = null;
    if (this.state.loginStatus === 'success') {
      loginButtonIcon = 'check-circle-o';
    } else if (this.state.loginStatus === 'fail') {
      loginButtonIcon = 'cross-circle';
    } else if (this.state.loginStatus === 'loading') {
      loginButtonIcon = 'loading';
    }
    let isLoading = this.state.loginStatus === 'loading';
    if (this.state.qq && this.state.token) {
      return (
        <div className="login-container">
          <Card bordered className="login-card">
            <p>您（{this.state.qq}）正在向小科绑定教务处~</p>
            <p>请输入教务处账号密码:</p>
            <Form onFinish={this.handleLogin}>
              <Form.Item
                name="id"
                label="学号"
                rules={[
                  {
                    type: 'string',
                    message: '请输入学号',
                  },
                  {
                    required: true,
                    message: '请输入学号',
                  },
                ]}
              >
                <Input onChange={this.handleIdInput} />
              </Form.Item>

              <Form.Item
                name="密码"
                label="密码"
                rules={[
                  {
                    required: true,
                    message: 'Please input your password!',
                  },
                ]}
                hasFeedback
              >
                <Input.Password onChange={this.handlePwdInput} />
              </Form.Item>
              <Form.Item
                valuePropName="checked"
                rules={[
                  {
                    validator: (_, value) =>
                      value
                        ? Promise.resolve()
                        : Promise.reject('Should accept agreement'),
                  },
                ]}
              >
                <Checkbox
                  checked={this.state.agreeDeal}
                  onChange={this.handleAgreeCheckboxClick}
                >
                  我已经阅读了
                  <Button type="link" onClick={this.click} size="small">
                    用户协议
                  </Button>
                  并同意。
                </Checkbox>
              </Form.Item>
              <Form.Item>
                <Button
                  disabled={
                    !this.state.stuId ||
                    !this.state.passwd ||
                    !this.state.agreeDeal ||
                    isLoading
                  }
                  type="primary"
                  htmlType="submit"
                  style={{ width: 320, marginLeft: 15 }}
                >
                  登录
                </Button>
              </Form.Item>
            </Form>
            <Modal
              visible={this.state.AgreeContentModalVisible}
              animationType="slide-up"
              title="用户协议"
              okText="我同意"
              cancelText="不同意"
              maskClosable="true"
              onCancel={this.onClose}
              onOk={this.handleAgreeButtonClick}
            >
              <Agreement />
            </Modal>
          </Card>
        </div>
      );
    } else {
      return <>参数错误</>;
    }
  }
}

export default App;
