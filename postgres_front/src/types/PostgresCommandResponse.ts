import PostgresResultResponse from '@/types/PostgreResultResponse'


interface PostgersCommandResponse {
  status: string,
  columns: string[] | null,
  results: PostgresResultResponse[],
  error: string
}

export default  PostgersCommandResponse
