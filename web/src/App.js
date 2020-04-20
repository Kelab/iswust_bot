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
import './App.less';
import axios from 'axios';
import queryString from 'query-string';
import configs from './config';
import { CloseWebPage } from './tools';

const AgreeItem = Checkbox.AgreeItem;

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
      nickname: '',
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
      nickname: url_.query.nickname || '',
      token: url_.query.token || '',
    });
  }
  onWrapTouchStart = e => {
    if (!/iPhone|iPod|iPad/i.test(navigator.userAgent)) {
      return;
    }
    const pNode = closest(e.target, '.am-modal-content');
    if (!pNode) {
      e.preventDefault();
    }
  };
  handleInput = key => value => {
    console.log('handleInput -> key: ', key);
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
        .post(configs.apiUrl + '/api/v1/user/bind', login_data)
        .then(res => {
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
        .catch(err => {
          if (err.response && err.response.status == 403) {
            Toast.fail('参数请求错误!', 1, null, false);
          } else {
            Toast.fail(
              `登录失败:${err.response.status}，请检查网络连接!`,
              1,
              null,
              false
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
  showModal = key => e => {
    e.preventDefault(); // 修复 Android 上点击穿透
    this.setState({
      [key]: true,
    });
  };
  onClose = key => () => {
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
    if (this.state.qq && this.state.nickname && this.state.token) {
      return (
        <WingBlank>
          <div className="App">
            {this.state.qq && (
              <div>
                <img
                  className="qq_avatar"
                  alt="avatar"
                  src={`http://q1.qlogo.cn/g?b=qq&nk=${this.state.qq}&s=640`}
                />
                <div
                  style={{
                    fontSize: '17',
                  }}
                >
                  {this.state.nickname &&
                    `${this.state.qq} · ${this.state.nickname}`}
                </div>
              </div>
            )}

            <List
              renderHeader={() => (
                <span>正在将 QQ 绑定至教务处，请输入教务处账号密码：</span>
              )}
            >
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
              <div
                style={{
                  minHeight: '100px',
                  maxHeight: '300px',
                  marginLeft: '10%',
                  marginRight: '10%',
                  overflow: 'scroll',
                  textAlign: 'left',
                }}
              >
                <b>
                  为使用QQ教务处软件（以下简称“本软件”）及服务，用户应当阅读并遵守《用户协议》（以下简称“本协议”）。请用户务必审慎阅读、充分理解各条款内容，特别是免除或者限制责任的条款，并选择接受或不接受。限制、免责条款可能以加粗形式提示用户注意。
                  除非用户已阅读并接受本协议所有条款，否则用户无权使用本软件及相关服务。用户的使用、登录等行为即视为用户已阅读并同意上述协议的约束。
                </b>
                <ul>
                  <ol>
                    我们承诺只在合法范围内使用您的教务处帐号，比如向您发送课表，发送新闻。
                  </ol>
                  <ol>我们不会在未经您的允许的情况下使用您的个人信息。</ol>
                  <ol>我们承诺会保护您的个人信息。</ol>
                </ul>
                <h3>用户注意事项</h3>
                用户理解并同意：为了向用户提供有效的服务，本软件会利用用户终端设备的处理器和带宽等资源。本软件使用过程中可能产生数据流量的费用，用户需自行向运营商了解相关资费信息，并自行承担相关费用。
                你理解并同意：本软件会让最终用户查询到本企业或组织内其他最终用户的信息，但管理员可以通过管理权限限制最终用户的信息查阅权限。在使用本服务管理你的最终用户信息时，你应当：
                充分告知最终用户使用本软件及本服务对用户信息、内容相关影响的政策规定；
                确保在使用本服务过程中对用户信息、内容的使用和处理遵从可适用的法律法规的要求;
                应对并处理你与最终用户就用户信息、内容相关的，或因你未完全履行该条款所产生的所有争议及纠纷，并独立承担由此而产生的一切法律责任。
                用户在使用本软件某一特定服务或功能时，可能会另有单独的协议、相关业务规则等。用户使用相关服务，即视为用户接受前述协议。
                用户理解并同意软件开发者将会尽其商业上的合理努力保障用户在本软件及服务中的数据存储安全，但是，开发者并不能就此提供完全保证，包括但不限于以下情形：
                <ul>
                  <ol>
                    开发者不对用户在本软件及服务中相关数据的删除或储存失败负责；
                  </ol>
                  <ol>
                    开发者有权根据实际情况自行决定用户在本软件及服务中数据的最长储存期限，并在服务器上为其分配数据最大存储空间等。
                  </ol>
                  <ol>
                    如果用户停止使用本软件及服务或服务被终止、取消，开发者可以从服务器上永久地删除你的数据。服务停止、终止或取消后，开发者没有义务向用户返还任何数据。
                  </ol>
                </ul>
                用户在使用本软件及服务时，须自行承担如下来自开发者不可掌控的风险内容，包括但不限于：
                <ul>
                  <ol>由于不可抗拒因素可能引起的用户信息丢失、泄漏等风险；</ol>
                  <ol>
                    用户在使用本软件访问第三方网站时，因第三方网站及相关内容所可能导致的风险，由用户自行承担；
                  </ol>
                  <ol>
                    用户发内容被他人转发、分享，因此等传播可能带来的风险和责任；
                  </ol>
                  <ol>
                    由于网络信号不稳定、网络带宽小等网络原因，所引起的登录失败、资料不完整、消息推送失败等风险。
                  </ol>
                </ul>
                当你同意本协议时，意味着我们已经有权使用您的帐号。
                最终解释权归本软件的开发者所有。
                <br />
              </div>
            </Modal>
          </div>
        </WingBlank>
      );
    }
    return <div>参数错误</div>;
  }
}

export default App;
