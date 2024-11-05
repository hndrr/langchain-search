type QuestionMessageProps ={
    content: string;
}

export const QuestionMessage: React.FC<QuestionMessageProps> = ({content}) => {
    return (
        <div className="py-2">
                <p className="text-3xl">
                    {content}
                </p>
        </div>
    );
}

