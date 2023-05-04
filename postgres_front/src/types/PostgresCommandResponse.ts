import PostgresResultResponse from '@/types/PostgreResultResponse'

interface PostgersCommandResponse {
    status: string
    columns: string[] | null
    result: PostgresResultResponse[]
    error_message: string
    command: string
}

export default PostgersCommandResponse
