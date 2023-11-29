import request from '@/utils/request'

export function getalllogs() {
  return request({
    url: '/api/log_manage/getalllogs',
    method: 'get'
  })
}