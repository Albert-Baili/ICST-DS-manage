import request from '@/utils/request'

export function get_local_ip() {
  return request({
    url: '/api/dashbord/getIP',
    method: 'get',
  })
}