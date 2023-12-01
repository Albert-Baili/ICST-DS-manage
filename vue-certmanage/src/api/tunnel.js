import request from '@/utils/request'

export function testtunnel(headerIn) {
  return request({
    url: '/api/test_tennel',
    method: 'get',
    headers:headerIn
  })
}

export function getalltunnel() {
  return request({
    url: '/api/tunnel_manage/getalltunnels',
    method: 'get'
  })
}

export function getallcert() {
  return request({
    url: '/api/certificates/getallcerts',
    method: 'get'
  })
}

  export function tunnelSend(data) {
    return request({
      url: '/api/tunnel_manage/sendinfo',
      method: 'post',
      data
    })
  }

  export function certDownloadByID(index) {
    return request({
      url: '/api/certificates/' + index,
      method: 'get'
    })
  }