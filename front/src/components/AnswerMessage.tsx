type AnswerMessageProps = {
    content: string;
}

export const AnswerMessage: React.FC<AnswerMessageProps> = ({ content }) => {
    return (
        <div className="py-2">
            <h2 className="text-lg font-bold pb-1">Answer</h2>
            <p className="text-base">
                {content} で検索
            </p>
        </div>
    );
}
