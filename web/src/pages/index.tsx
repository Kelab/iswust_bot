import React, { useEffect, useState } from 'react';
import { DefaultHeader } from '@ant-design/pro-layout';
import './index.less';
import { getUserFromQuery } from './tools';

export default (props) => {
  const [qq, setQQ] = useState('');
  const [token, setToken] = useState('');

  useEffect(() => {
    const user = getUserFromQuery();
    setQQ(user.qq as string);
    setToken(user.token as string);
  });

  return (
    <div>
      <DefaultHeader
        collapsedButtonRender={() => null}
        navTheme="light"
        rightContentRender={() => <>{qq}</>}
      />
      {props.children}
    </div>
  );
};
