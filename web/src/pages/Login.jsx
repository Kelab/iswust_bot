import {
  Button,
  Checkbox,
  InputItem,
  List,
  WhiteSpace,
  WingBlank,
  Toast,
  Modal,
} from 'antd-mobile';
import React from 'react';
import './Login.less';
import axios from 'axios';
import queryString from 'query-string';
import configs from './config';
import Agreement from '../components/Agreement';

const { AgreeItem } = Checkbox;

function closest(el, selector) {
  const matchesSelector =
    el.matches ||
    el.webkitMatchesSelector ||
    el.mozMatchesSelector ||
    el.msMatchesSelector;
  while (el) {
    if (matchesSelector.call(el, selector)) {
      return el;
    }
    el = el.parentElement;
  }
  return null;
}

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      qq: '',
      stuId: '',
      passwd: '',
      token: '',
      agreeDeal: false,
      loginStatus: null,
      AgreeContentModalVisible: false,
    };
  }
  componentDidMount() {
    let url_ = queryString.parseUrl(window.location.href);

    this.setState({
      qq: url_.query.qq || '',
      token: url_.query.token || '',
    });
  }

  onWrapTouchStart = (e) => {
    if (!/iPhone|iPod|iPad/i.test(navigator.userAgent)) {
      return;
    }
    const pNode = closest(e.target, '.am-modal-content');
    if (!pNode) {
      e.preventDefault();
    }
  };

  handleInput = (key) => (value) => {
    this.setState({
      [key]: value,
    });
  };

  handleLogin = () => {
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
            Toast.success(`登录成功！请返回聊天页面。`, 0, null, false);
            this.setState({
              loginStatus: 'success',
            });
          } else if (res.status == '200' && res.data.code == '-1') {
            if (res.data.data == 'qq绑定失败!失败原因是AuthFail') {
              Toast.fail(`绑定失败！用户名密码错误！`, 2, null, false);
            } else if (res.data.data == '该qq已经绑定了!') {
              Toast.fail(`该 QQ 已绑定！`);
            } else {
              Toast.fail(`绑定失败，教务处暂时无法访问！`, 2, null, false);
            }
            this.setState({
              loginStatus: 'fail',
            });
          }
        })
        .catch((err) => {
          if (err.response && err.response.status == 403) {
            Toast.fail('参数请求错误!', 1, null, false);
          } else {
            Toast.fail(
              `登录失败:${err.response.status}，请检查网络连接!`,
              1,
              null,
              false,
            );
          }
          this.setState({
            loginStatus: 'fail',
          });
        });
    } else {
      Toast.fail('请输入账号密码！', 1, null, false);
    }
  };

  showModal = (key) => (e) => {
    e.preventDefault(); // 修复 Android 上点击穿透
    this.setState({
      [key]: true,
    });
  };

  onClose = (key) => () => {
    this.setState({
      [key]: false,
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

  render() {
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
        <WingBlank>
          <div className="App">
            <div
              style={{
                fontSize: '2em',
                textAlign: 'left',
              }}
            >
              请输入教务处账号密码：
            </div>
            <List>
              <InputItem
                labelNumber={3}
                placeholder="请输入学号"
                value={this.state.stuId}
                onChange={this.handleInput('stuId')}
              >
                学号
              </InputItem>
              <InputItem
                labelNumber={3}
                placeholder="请输入密码"
                type="password"
                value={this.state.passwd}
                onChange={this.handleInput('passwd')}
              >
                密码
              </InputItem>
            </List>
            <WhiteSpace />
            <AgreeItem
              checked={this.state.agreeDeal}
              onChange={this.handleAgreeCheckboxClick}
            >
              我已阅读并同意
              <a
                href="modal"
                className="link"
                onClick={this.showModal('AgreeContentModalVisible')}
              >
                用户协议
              </a>
              。
            </AgreeItem>
            <Button
              disabled={
                !this.state.stuId ||
                !this.state.passwd ||
                !this.state.agreeDeal ||
                isLoading
              }
              onClick={this.handleLogin}
              icon={loginButtonIcon}
            >
              登录
            </Button>
            <Modal
              popup
              visible={this.state.AgreeContentModalVisible}
              animationType="slide-up"
              onClose={this.onClose('AgreeContentModalVisible')}
              title="用户协议"
              footer={[
                {
                  text: '我已阅读并同意',
                  onPress: () => {
                    this.handleAgreeButtonClick();
                  },
                },
              ]}
              wrapProps={{ onTouchStart: this.onWrapTouchStart }}
            >
              <Agreement />
            </Modal>
          </div>
        </WingBlank>
      );
    }
    return <div>参数错误</div>;
  }
}

export default App;
