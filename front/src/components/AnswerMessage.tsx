type AnswerMessageProps = {
    content: string;
}

export const AnswerMessage: React.FC<AnswerMessageProps> = ({ content }) => {
    return (
        <div className="py-2">
            <h2 className="text-gray-500">Answer</h2>
            <p className="text-gray-500">
                {content} で検索
            </p>
        </div>
    );
}
