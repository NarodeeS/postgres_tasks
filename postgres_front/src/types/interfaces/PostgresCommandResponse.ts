import PostgresResultResponse from '@/types/interfaces/PostgreResultResponse'

interface PostgersCommandResponse {
    status: string
    columns: string[] | null
    result: PostgresResultResponse[]
    error_message: string
    command: string
}

export default PostgersCommandResponse
