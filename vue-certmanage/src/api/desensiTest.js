import request from '@/utils/request'


  export function sendDesensiTest_yangai(data) {
    return request({
      url: '/api/sendDesensiTest/yangai',
      method: 'post',
      data
    })
  }


  export function sendDesensiTest_hash(data) {
    return request({
      url: '/api/sendDesensiTest/hash',
      method: 'post',
      data
    })
  }
  

  export function sendDesensiTest_enc(data) {
    return request({
      url: '/api/sendDesensiTest/des',
      method: 'post',
      data
    })
  }