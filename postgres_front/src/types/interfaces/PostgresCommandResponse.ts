import PostgresResultResponse from '@/types/interfaces/PostgreResultResponse'

interface PostgersCommandResponse {
    status: string
    columns: string[] | null
    result: PostgresResultResponse[]
    errorMessage: string
    command: string
}

export default PostgersCommandResponse
