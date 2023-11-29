import request from '@/utils/request'


  export function sendDesensiTest_yangai(data) {
    return request({
      url: '/api/sendDesensiTest/yangai',
      method: 'post',
      data
    })
  }
