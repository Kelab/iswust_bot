import React from 'react';
import {
  AlertOutlined,
  BellOutlined,
  BulbOutlined,
  DollarCircleOutlined,
  DotChartOutlined,
  GithubOutlined,
  NodeExpandOutlined,
  ProfileOutlined,
  ScheduleOutlined,
  SendOutlined,
} from '@ant-design/icons';
import { Button, Card, Checkbox, List, message, Switch } from 'antd';
import axios from 'axios';
import RSS from '../components/icons/RSS';
import configs from './config';
import { getUserFromQuery } from './tools';
import './UserCenter.less';

const CheckboxGroup = Checkbox.Group;
export default class UserCenter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      qq: '',
      token: '',
      loading: false,
      subdata: {},
    };
  }

  componentDidMount() {
    const user = getUserFromQuery();
    this.setState(
      {
        qq: user.qq,
        token: user.token,
      },
      () => {
        axios
          .get(configs.apiUrl + '/api/subs', {
            params: { qq: this.state.qq, token: this.state.token },
          })
          .then((res) => {
            this.setState({
              subdata: res.data || [],
            });
          });
      },
    );
  }
  renderFuncItem = ({ name, Icon, iconColor, iconBackgroundColor }) => (
    <List.Item>
      <Card
        className="func-item"
        style={{
          borderColor: iconBackgroundColor + '40',
        }}
        bordered={false}
        bodyStyle={{
          padding: 'unset',
          display: 'flex',
          alignItems: 'center',
          flexDirection: 'column',
        }}
      >
        <div
          className="func-item-icon"
          style={{
            backgroundColor: iconBackgroundColor,
          }}
        >
          <Icon style={{ color: iconColor || '#ffffff' }} />
        </div>
        <h3 className="func-item-name">{name}</h3>
      </Card>
    </List.Item>
  );

  renderSubItem = ({ name, enable }) => (
    <List.Item className="subitem">
      <Switch
        className="switch"
        defaultChecked={enable}
        onClick={(event) => this.handleSwitchClick(event, name)}
        loading={this.state.loading}
      />
      <h3 className="content">{name}</h3>
    </List.Item>
  );

  handleSwitchClick = (event, name) => {
    this.setState({
      loading: true,
    });
    let postdata = {};
    for (let item in this.state.subdata.data) {
      if (this.state.subdata.data[item].name === name) {
        postdata[item] = event;
      }
    }
    axios({
      method: 'post',
      url: configs.apiUrl + '/api/subs',
      params: { qq: this.state.qq, token: this.state.token },
      data: postdata,
    })
      .then((res) => {
        this.setState({
          loading: false,
        });
        let key = Object.keys(res.data.data);
        let msg = res.data.data[key].msg;
        message.success(msg);
      })
      .catch((err) => {
        message.error('当前出错了，请稍后再试');
      });
  };

  render() {
    let options = [];
    for (let item in this.state.subdata.data) {
      options.push(this.state.subdata.data[item]);
    }
    return (
      <div className="container">
        <div className="subscriptions">
          <Card title="订阅">
            <List
              grid={{
                gutter: 24,
                xs: 1,
                sm: 1,
                md: 2,
                lg: 2,
                xl: 3,
                xxl: 3,
              }}
              dataSource={options}
              renderItem={this.renderSubItem}
            />
          </Card>
        </div>
        <div className="function">
          <Card
            title="功能"
            extra={
              <Button
                href="https://bot.artin.li/guide/"
                target="_blank"
                type="link"
              >
                帮助
              </Button>
            }
          >
            <List
              header="教务相关功能"
              grid={{
                gutter: 32,
                xs: 3,
                sm: 3,
                md: 4,
                lg: 4,
                xl: 6,
                xxl: 6,
              }}
              dataSource={[
                {
                  name: '绑定教务处',
                  Icon: NodeExpandOutlined,
                  iconBackgroundColor: '#f77dc2',
                },
                {
                  name: '查询绩点',
                  Icon: DotChartOutlined,
                  iconBackgroundColor: '#0288d1',
                },
                {
                  name: '订阅通知',
                  Icon: BellOutlined,
                  iconBackgroundColor: '#00796b',
                },
                {
                  name: '查询课表',
                  Icon: ProfileOutlined,
                  iconBackgroundColor: '#a95ec7',
                },

                {
                  name: '查询成绩',
                  Icon: SendOutlined,
                  iconBackgroundColor: '#afb42b',
                },
                {
                  name: '饭卡余额',
                  Icon: DollarCircleOutlined,
                  iconBackgroundColor: '#455a64',
                },
              ]}
              renderItem={this.renderFuncItem}
            />
            <List
              header="其他"
              grid={{
                gutter: 32,
                xs: 3,
                sm: 3,
                md: 4,
                lg: 4,
                xl: 6,
                xxl: 6,
              }}
              dataSource={[
                {
                  name: '计划提醒',
                  Icon: BulbOutlined,
                  iconBackgroundColor: '#2cddbe',
                },
                {
                  name: '托管日历',
                  Icon: ScheduleOutlined,
                  iconBackgroundColor: '#f3d768',
                },
                {
                  name: '运行代码',
                  Icon: GithubOutlined,
                  iconBackgroundColor: '#0097a7',
                },
                {
                  name: '订阅 RSS',
                  Icon: AlertOutlined,
                  iconBackgroundColor: '#86D4F5',
                },
                {
                  name: '一言',
                  Icon: RSS,
                  iconBackgroundColor: '#0097a7',
                },
              ]}
              renderItem={this.renderFuncItem}
            />
          </Card>
        </div>
      </div>
    );
  }
}
