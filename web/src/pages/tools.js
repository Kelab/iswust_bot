import queryString from 'query-string';

export function CloseWebPage() {
  if (navigator.userAgent.indexOf('MSIE') > 0) {
    if (navigator.userAgent.indexOf('MSIE 6.0') > 0) {
      window.opener = null;
      window.close();
    } else {
      window.open('', '_top');
      window.top.close();
    }
  } else if (
    navigator.userAgent.indexOf('Firefox') > 0 ||
    navigator.userAgent.indexOf('Chrome') > 0
  ) {
    //window.location.href = 'about:blank ';
    window.location.href = 'about:blank';
    window.close();
  } else {
    window.opener = null;
    window.open('', '_self');
    window.close();
  }
}

export const getUserFromQuery = () => {
  let b64 = window.location.search.substring(1);
  try {
    let query = window.atob(b64);
    let parsedQuery = queryString.parse(query);
    return {
      qq: parsedQuery.qq || '',
      token: parsedQuery.token || '',
    };
  } catch (error) {
    return {};
  }
};
