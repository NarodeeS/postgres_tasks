import PostgresResultResponse from '@/types/PostgreResultResponse'


interface PostgersCommandResponse {
  status: string,
  columns: string[] | null,
  result: PostgresResultResponse[],
  error_message: string
}

export default  PostgersCommandResponse
